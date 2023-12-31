from gpt_search import *
from ingest import *
from fact_sheet import *

def commands(index_name, embeddings):
    query_text = ' '

    while query_text != '':
        print("Enter a command:\n(1) Process PDFs\n(2) Ask a question\n(3) Process a fact sheet\n(4) Retrieve legal documents\n(5) Quit\n")
        query_text = input("Command selected is: ")
        if (query_text == "Process PDFs" or query_text == "1"):
            print("Procedure for Processing PDFs.")
            pdf_directory = input("Directory for PDFs to be processed is: ")
            include_name_space = input("Would you like to include a namespace argument?\n(1) Yes\n(2) No\n")
            if (include_name_space == "Yes" or include_name_space == "yes" or include_name_space == "y" or include_name_space == "1"):
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
            name_space = ""
            # Ask whether wishes to include a namespace?
            include_name_space = input("Would you like to identify a namespace argument?\n(1) Yes\n(2) No\n")
            if (include_name_space == "Yes" or include_name_space == "yes" or include_name_space == "y" or include_name_space == "1"):
                name_space = input("What is the namespace?: ")
            query_result = chat_with_index(query_text, index_name, embeddings, name_space)
            print(query_result)
            continue
        if (query_text == "3"):
            name_space = ""
            #fact_pattern = input("Please input fact pattern: ")
            #fact_pattern = "•	Client is Allison. She and her partner are from Canada. •	Allison is sexually active with her partner Daniel. •	Daniel and Allison have been having sex for 14 months. •	Prior to meeting Allison, Daniel discovered he had syphilis. •	Daniel did not tell client Allison that he has syphilis, because he thought she would not agree to have sex with him if he did. •	Daniel and Allison continued having sexual intercourse. •	Allison has recently discovered that she contracted syphilis from Daniel. •	Allison would not have continued having sex with Daniel had she known he had syphilis."
            # question = f'Within the triple quotes is a legal fact pattern. """{fact_pattern}""". Referring only to Canadian criminal law, return a list of legal issues idenfitied in the fact pattern. Each legal issue should only be one or two words.'
            query_result = issue_spot()
            print(query_result)
            # include_name_space = input("Would you like to identify a namespace argument?\n(1) Yes\n(2) No\n")
            # if (include_name_space == "Yes" or include_name_space == "yes" or include_name_space == "y" or include_name_space == "1"):
            #     name_space = input("What is the namespace?: ")
            # query_result = search(question, index_name, embeddings, name_space)
            # print(query_result)
            continue
        if (query_text == "4"):
            continue
        if (query_text == "Quit" or query_text == "quit" or query_text == "5"):
            print("Program exiting. Bye.")
            break
        else:
            print("Invalid selection. Please try again.\n")
            continue