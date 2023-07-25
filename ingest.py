import os
import ssl
import nltk
import sys
import pinecone
from PyPDF2 import PdfReader
from langchain.llms import OpenAI
from langchain.chains import ConversationChain, LLMChain, RetrievalQAWithSourcesChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from langchain.agents import load_tools, initialize_agent
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from nltk import word_tokenize,sent_tokenize

"""
# API keys
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "4dfd323ac4be946c150a8824d528a68e9b9b7d213dc84415213269fecaea78b4"
os.environ["PINECONE_API_KEY"] = "0da32401-269e-483a-9e49-482ffd544132"

# Initialize NLTK tokenization engine
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Initialize Pinecone vector DB
pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment="northamerica-northeast1-gcp"
)
index_name = "test2"

# Initialize OpenAI props
embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))
"""

def pdf_to_doc(directory):
    docs = []

    # Convert each PDF file into LangChain doc
    for pdf_file in os.listdir(directory):
        doc = Document(page_content="text", metadata={"source": "local"})
        doc.page_content = ""
        pdf_reader = PdfReader(directory+'/'+pdf_file)
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

# TODO: consider how to incorporate name_spaces into the process PDF portion
def process_pdfs(directory, embeddings, index_name, name_space):
 
    # Step 1: convert PDF files into langchain docs
    docs = pdf_to_doc(directory)

    # Step 2: split docs into text blocks
    text_blocks = docs_to_blocks(docs)

    # Step 3: generate metadata for blocks
    meta = generate_doc_metadata(text_blocks)

    vectorstore = Pinecone.from_texts([t.page_content for t in text_blocks], embedding=embeddings, 
                                      batch_size= 256, metadatas=meta, index_name=index_name, namespace=name_space)

       

    return vectorstore

def main():
    pinecone_index = []

    if len(sys.argv) != 3:
        sys.exit("Usage: program folder namespace")

    print("Folder name:", sys.argv[1])
    print("Namespace:", sys.argv[2])

    # Call processing function
    process_pdfs(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()