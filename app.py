import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
# from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.chat_models import ChatOpenAI
from htmlTemplates import css, bot_template, user_template
from langchain.vectorstores import Pinecone
import pinecone

# https://www.youtube.com/watch?v=dXxQ0LR-3Hg
# streamlit run app.py

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
pinecone.init(api_key= PINECONE_API_KEY, environment="northamerica-northeast1-gcp")


def get_pdf_data(pdf_docs):

    docs = []
    for pdf in pdf_docs:
        doc = Document(page_content="text", metadata={"source": "local"})
        doc.page_content = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            doc.page_content += page.extract_text()
        doc.metadata = pdf.name
        docs.append(doc)
    return docs



def get_text_blocks(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function = len)
    text_blocks = []
    for doc in docs:
        split_content = text_splitter.split_text(doc.page_content)
        for content in split_content:
            new_doc = Document(page_content="text", metadata={"source": "local"})
            new_doc.page_content = content
            new_doc.metadata = doc.metadata    
            text_blocks.append(new_doc)
    return text_blocks
    


def get_vectorstore(doc_blocks):
    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
    meta = []
    for block in doc_blocks:
        block_dict = {'source': block.metadata}
        meta.append(block_dict)

    vectorstore = Pinecone.from_texts([t.page_content for t in doc_blocks], embedding=embeddings, metadatas=meta, index_name="test2")    
    return vectorstore

# def get_vectorstore(text_chunks):
#     embeddings = OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'))
#     # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
#     # vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#     vectorstore = Pinecone.from_texts([t for t in text_chunks], embedding=embeddings, index_name="test")
#     return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(temperature=0.2)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        memory=memory
    )
    
    return conversation_chain

# def handle_environment():
#     load_dotenv()
#     PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
#     #print(PINECONE_API_KEY)
#     pinecone.init(api_key= PINECONE_API_KEY, environment="northamerica-northeast1-gcp")


def handle_userinput(user_question):
    
    response = st.session_state.conversation({'question': user_question})
    print(response)
    # print(response['answer'])
    # print("question: " + response['question'])
    # print(response['chat_history'])
    # print(response['source_documents'][0].metadata['source'])
    # + " Sources: " + response['source_documents'][0].metadata['source'])
    # print(len(response.keys()))
    sources = ""

    if (len(response.keys()) == 4):
        if (response['source_documents'][0].metadata):
            sources = response['source_documents'][0].metadata['source']

    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content + " Source: " + sources), unsafe_allow_html=True)



def main():
    
    # handle_environment()
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)


    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    #st.write(user_template.replace("{{MSG}}", "hello robot"), unsafe_allow_html=True)
    #st.write(bot_template.replace("{{MSG}}", "hello human"), unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                documents = get_pdf_data(pdf_docs)
                
                # get text chunks
                document_blocks = get_text_blocks(documents)

                # create vector store
                vectorstore = get_vectorstore(document_blocks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)
    



    

if __name__ == '__main__':
    main()
