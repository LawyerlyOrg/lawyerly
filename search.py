import sys
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI

# def eval(index_name, embeddings, name_space, question):
#     index = getExistingIndex(index_name, embeddings, name_space)
#     result = index.query(vector=index, queries=question, namespace=name_space, filter= )
#     return result

def search(query, index, meta_filter={}):
    #index = getExistingIndex(index_name, embeddings, name_space)
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        llm=OpenAI(temperature=0.0), chain_type="stuff", retriever=index.as_retriever(search_kwargs={'filter': meta_filter}))
    result = chain({'question': query}, return_only_outputs=True)
    return result

def get_existing_index(index_name, embeddings, name_space=""):
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
