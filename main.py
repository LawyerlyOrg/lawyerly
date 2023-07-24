# hello Monir, I am a ghostimport os
from search import *
from ingest import *

# API keys
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "4dfd323ac4be946c150a8824d528a68e9b9b7d213dc84415213269fecaea78b4"
os.environ["PINECONE_API_KEY"] = "0da32401-269e-483a-9e49-482ffd544132"

# Initialize OpenAI props
embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))

# Initialize Pinecone vector DB
pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment="northamerica-northeast1-gcp"
)
index_name = "test2"

def main():
    process_pdfs(directory='pdf_peeshee', index_name=index_name, embeddings=embeddings, name_space='test2')
    #print(search("are peeshees animals?", index_name=index_name, embeddings=embeddings, name_space='peeshee'))

if __name__ == '__main__':
    main()
