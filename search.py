import os
import sys
import pinecone
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI

"""
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
"""

def search(query, index_name, embeddings, name_space=""):
    index = getExistingIndex(index_name, embeddings, name_space)
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=OpenAI(temperature=0), chain_type="stuff", retriever=index.as_retriever())
    result = chain({'question': query}, return_only_outputs=True)
    return result

def getExistingIndex(index_name, embeddings, name_space=""):
    if not name_space:
        pindex = Pinecone.from_existing_index(
        index_name=index_name, embedding=embeddings)
    else:
        pindex = Pinecone.from_existing_index(
            index_name=index_name, embedding=embeddings, namespace=name_space)
    return pindex

def main():

    if len(sys.argv) != 3:
        sys.exit("Usage: program folder namespace")

    print("Query", sys.argv[1])
    print("Namespace:", sys.argv[2])

    pinecone_index = getExistingIndex(sys.argv[2])
    print('new index is', pinecone_index)
    #new index is <langchain.vectorstores.pinecone.Pinecone object at 0x1100cb750>
    response = search(sys.argv[1], pinecone_index)
    print(response)


if __name__ == '__main__':
    main()