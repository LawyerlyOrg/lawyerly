# hello Monir, I am a ghostimport os
from search import *
from ingest import *
from dotenv import load_dotenv

# API keys
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

# Initialize OpenAI props
embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get('OPENAI_API_KEY'))

# Initialize Pinecone vector DB
pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment="northamerica-northeast1-gcp"
)
index_name = "test2"

def main():
    #process_pdfs(directory='pdf_peeshee', index_name=index_name, embeddings=embeddings, name_space='test2')
    #print(search("are peeshees animals?", index_name=index_name, embeddings=embeddings, name_space='peeshee'))
    #pinecone_index = []

    # Perform sample search
    #query_text = "List the titles of the legal cases in bullet point form."
    query_text = ' '

    while query_text != '':
        print("Enter a command:\n(1) Process PDFs\n(2) Ask a question\n(3) Process a fact sheet\n(4) Quit\n")
        query_text = input("Command selected is: ")
        if (query_text == "Process PDFs" or query_text == "1"):
            print("Procedure for Processing PDFs.")
            pdf_directory = input("Directory for PDFs to be processed is: ")
            include_name_space = input("Would you like to include a namespace parameter?\n(1) Yes\n(2) No\n")
            if (include_name_space == "Yes" or include_name_space == "y" or include_name_space == "1"):
                name_space = input("What is the namespace?: ")
                print("Processing PDFs.")
                process_pdfs(pdf_directory, index_name, embeddings, name_space)
            else:
                print("Processing PDFs.")
                process_pdfs(pdf_directory, index_name, embeddings)
            print("PDFs have been processed")
            continue
        if (query_text == "Ask a question" or query_text == "2"):
            query_text = input("Ask your question: ")
            # Ask whether wishes to include a namespace?
            include_name_space = input("Would you like to include a namespace parameter?\n(1) Yes\n(2) No\n")
            if (include_name_space == "Yes" or include_name_space == "y" or include_name_space == "1"):
                name_space = input("What is the namespace?: ")
                print('your namespace is', name_space)
                #pinecone_index = getExistingIndex(name_space)
                query_result = search(query_text, index_name, embeddings, name_space)
                print(query_result)
            # else:
            #     pinecone_index = getExistingIndex()
            #query_result = search(query_text, pinecone_index)
            #print(query_result)
            continue
        if (query_text == "3"):
            fact_pattern = "•	Client is Allison. She and her partner are from Canada. •	Allison is sexually active with her partner Daniel. •	Daniel and Allison have been having sex for 14 months. •	Prior to meeting Allison, Daniel discovered he had syphilis. •	Daniel did not tell client Allison that he has syphilis, because he thought she would not agree to have sex with him if he did. •	Daniel and Allison continued having sexual intercourse. •	Allison has recently discovered that she contracted syphilis from Daniel. •	Allison would not have continued having sex with Daniel had she known he had syphilis."
            question = f'Within the triple quotes is a legal fact pattern. """{fact_pattern}""". Based on the legal fact pattern, return the names of the most relevant cases, and their summaries.'
            include_name_space = input("Would you like to include a namespace parameter?\n(1) Yes\n(2) No\n")
            if (include_name_space == "Yes" or include_name_space == "y" or include_name_space == "1"):
                name_space = input("What is the namespace?: ")
                #pinecone_index = getExistingIndex(name_space)
                query_result = search(question, index_name, embeddings, name_space)
                print(query_result)
                
            # else:
            #     pinecone_index = getExistingIndex()
            # query_result = search(question, pinecone_index)
            # print(query_result)
            continue
        if (query_text == "Quit" or query_text == "quit" or query_text == "4"):
            print("Program exiting. Bye.")
            break
        else:
            print("Invalid selection. Please try again.\n")
            continue

if __name__ == '__main__':
    main()
