from search import *
from ingest import *
from factsheet import *
from commands import *
import constants

# API keys
OPENAI_API_KEY = constants.OPENAI_API_KEY
PINECONE_API_KEY = constants.PINECONE_API_KEY
SERPAPI_API_KEY = constants.SERPAPI_API_KEY

# Store API keys in OS env
os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY
os.environ["SERPAPI_API_KEY"] = constants.SERPAPI_API_KEY
os.environ["PINECONE_API_KEY"] = constants.PINECONE_API_KEY

# Initialize OpenAI props
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
openai.api_key = OPENAI_API_KEY

# Initialize Pinecone vector DB
pinecone.init(
    api_key=PINECONE_API_KEY,
    environment="northamerica-northeast1-gcp"
)
index_name = "test2"

def main():
    #commands(index_name, embeddings)
    print(issue_spot())

if __name__ == '__main__':
    main()
