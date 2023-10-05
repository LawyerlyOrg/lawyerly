import os
import openai
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
#import constants

def pytest_configure(config):
    embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
    openai.api_key = os.environ["OPENAI_API_KEY"]
    pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment="northamerica-northeast1-gcp"
    )