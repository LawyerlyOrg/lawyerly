import os
from PyPDF2 import PdfReader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
import prompts
from gpt_search import *
from db import *

def pdfs_to_doc(folder_path):
    docs = []

    # Convert each PDF file into LangChain doc
    for pdf_file in os.listdir(folder_path):
        pdf_file_path = folder_path+'/'+pdf_file
        doc = Document(page_content="text", metadata={"source": "local"})
        doc.page_content = ""
        pdf_reader = PdfReader(pdf_file_path)
        for page in pdf_reader.pages:
            doc.page_content += page.extract_text()
        doc.metadata = pdf_file
        docs.append(doc)

    return docs

def docs_to_blocks(docs):
    text_blocks = []
    # Split doc text into blocks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function = len)
    for doc in docs:
        split_content = text_splitter.split_text(doc.page_content)
        for content in split_content:
            new_doc = Document(page_content="text", metadata={"source": "local"})
            new_doc.page_content = content
            new_doc.metadata = doc.metadata    
            text_blocks.append(new_doc)
    return text_blocks

def generate_doc_metadata(text_blocks):
    meta = []
    for block in text_blocks:
        block_dict = {'source': block.metadata}
        meta.append(block_dict)

    return meta

def pdf_to_string(pdf_file_path):
    pdf_text = ""
    pdf_reader = PdfReader(pdf_file_path)

    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

    pdf_string = pdf_text

    return pdf_string

def extract_summary(law_area, index_name, file_name):
    query = prompts.prompt_dict[law_area]

    return chat_with_index(query, index_name, file_name)['answer']

# TODO: consider how to incorporate name_spaces into the process PDF portion
def process_pdfs(directory, embeddings, index_name, collection_name, law_area, user_email):
 
    # Step 1: convert PDF files into langchain docs
    docs = pdfs_to_doc(directory)

    # Step 2: split docs into text blocks
    text_blocks = docs_to_blocks(docs)

    # Step 3: generate metadata for blocks
    meta = generate_doc_metadata(text_blocks)

    # Step 4: store documents in Pinecone
    # TODO: ensure success/ failure of Pinecone.from_texts is coordinated with saving summary to db
    # i.e. both fail or both succeed.
    Pinecone.from_texts([t.page_content for t in text_blocks], embedding=embeddings, 
                                      batch_size= 256, metadatas=meta, index_name=index_name, namespace=collection_name)

    
    # Step 5: generate and store case summaries for each PDF file
    index = get_existing_index(index_name, embeddings, collection_name)

    for doc in docs:
        file_name = doc.metadata
        # summarize
        summary = extract_summary(law_area, index, file_name)
        print(f'Summary of {file_name}: {summary}')
        # store in DB\

    # Step 6: call DB operations
    case_summary_db_operations(user_email, collection_name, file_name, summary, )


