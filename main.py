import os
import ssl
import nltk
import pinecone
from langchain.llms import OpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from langchain.agents import load_tools, initialize_agent
from langchain.document_loaders import UnstructuredPDFLoader, OnlinePDFLoader
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
llm = OpenAI(temperature=0.9)

# Initialize Pinecone vector DB
pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment="northamerica-northeast1-gcp"
)
index_name = "langchain2"

def load_pdf_data(path):
    loader = UnstructuredPDFLoader(path)
    data = loader.load()
    return data

def split_pdf(pdf_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(pdf_data)
    return texts

def index_data(texts, embeddings, index_name):
    docsearch = Pinecone.from_texts([t.page_content for t in texts], embeddings, index_name=index_name)
    return docsearch

def process_pdfs(directory):
    docs = []
    chunked_docs = []

    # Load all PDF files in directory
    for pdf_file in os.listdir(directory):
        f = os.path.join(directory, pdf_file)
        docs.append(load_pdf_data(f))

    # Chunk PDF text
    for doc in docs:
        chunked_docs.append(split_pdf(doc))

    # Create 1D list of concatenated chunks
    concat_chunks = []
    for doc in chunked_docs: # Each individual doc is split into chunks
        for chunk in doc: # Each chunk contains page_content and metadata
            #print(chunk.page_content)
            #print('----------------------------------------------')
            #print(chunk.metadata)
            #print('\n')
            #print('\n')
            concat_chunks.append(chunk)

    # Index text chunks into Pinecone
    pinecone_index = index_data(concat_chunks, embeddings=embeddings, index_name=index_name)
    return pinecone_index

def search(query, index):
    docs = index.similarity_search(query)
    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.run(input_documents=docs, question=query)
    return result

def main():
    # Process all PDFs and create Pinecone index
    pinecone_index = process_pdfs('pdfs')

    # Perform sample search
    #query_text = "List the titles of the legal cases in bullet point form."
    query_text = ' '

    while query_text != '':
        query_text = input("Ask a question: ")
        query_result = search(query_text, pinecone_index)
        print(query_result)

if __name__ == "__main__":
    main()
    