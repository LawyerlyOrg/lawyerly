import os
import ssl
import nltk
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

# Initialize OpenAI props
embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))

# Initialize Pinecone vector DB
pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment="northamerica-northeast1-gcp"
)
index_name = "test2"

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
def process_pdfs(directory, name_space=""):
 
    # Step 1: convert PDF files into langchain docs
    docs = pdf_to_doc(directory)

    # Step 2: split docs into text blocks
    text_blocks = docs_to_blocks(docs)

    # Step 3: generate metadata for blocks
    meta = generate_doc_metadata(text_blocks)

    # Step 4: create Pinecone vector store
    # this is where the request rate limit is being triggered
    # TODO: rate limit being hit - consider backoff + batching (batching size increased to 256)
    vectorstore = Pinecone.from_texts([t.page_content for t in text_blocks], embedding=embeddings, 
                                      batch_size= 256, metadatas=meta, index_name=index_name, namespace=name_space)

    # vectorstore = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)
    # vectorstore.add_texts([t.page_content for t in text_blocks],
    #                    batch_size=256, metadatas=meta, namespace=name_space)
       

    return vectorstore

def search(query, index):
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=OpenAI(temperature=0), chain_type="stuff", retriever=index.as_retriever())
    result = chain({'question': query}, return_only_outputs=True)
    return result

def getExistingIndex(name_space=""):
    pindex = Pinecone.from_existing_index(
        index_name=index_name, embedding=embeddings, namespace=name_space)
    return pindex

# TODO: separate querying operation from indexing operation
def main():
    # Process all PDFs into Pinecone index
    #pinecone_index = process_pdfs('pdf_test')

    pinecone_index = []

    # Perform sample search
    #query_text = "List the titles of the legal cases in bullet point form."
    query_text = ' '

    while query_text != '':
        print("Enter a command:\n(1) Process PDFs\n(2) Ask a question\n(3) Quit\n")
        query_text = input("Command selected is: ")
        if (query_text == "Process PDFs" or query_text == "1"):
            print("Procedure for Processing PDFs.")
            pdf_directory = input("Directory for PDFs to be processed is: ")
            include_name_space = input("Would you like to include a namespace parameter?\n(1) Yes\n(2) No\n")
            if (include_name_space == "Yes" or include_name_space == "y" or include_name_space == "1"):
                name_space = input("What is the namespace?: ")
                print("Processing PDFs.")
                pinecone_index = process_pdfs(pdf_directory, name_space)
            else:
                print("Processing PDFs.")
                pinecone_index = process_pdfs(pdf_directory)
            print("PDFs have been processed")
            continue
        if (query_text == "Ask a question" or query_text == "2"):
            query_text = input("Ask your question: ")
            # Ask whether wishes to include a namespace?
            include_name_space = input("Would you like to include a namespace parameter?\n(1) Yes\n(2) No\n")
            if (include_name_space == "Yes" or include_name_space == "y" or include_name_space == "1"):
                name_space = input("What is the namespace?: ")
                pinecone_index = getExistingIndex(name_space)
            else:
                pinecone_index = getExistingIndex()
            query_result = search(query_text, pinecone_index)
            print(query_result)
            continue
        if (query_text == "Quit" or query_text == "quit" or query_text == "3"):
            print("Program exiting. Bye.\n")
            break
        else:
            print("Invalid selection. Please try again.\n")
            continue
        # query_text = input("Ask a question: ")
        # query_result = search(query_text, pinecone_index)
        # print(query_result)

if __name__ == "__main__":
    main()
    