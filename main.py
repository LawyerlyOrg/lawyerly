from search import *
from ingest import *
from factsheet import *
from commands import *
from evaluate_cases import *
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
    sample_fact_sheet = """
• Victim is Allison.  She and her partner are from Canada.  
• Allison is sexually active with her partner the defendant Daniel.  
• Daniel and Allison have been having sex for 14 months.  
• Prior to meeting Allison , Daniel discovered he had syphilis.  
• Daniel did not tell client Allison that he has syphilis , because he thought she would not agree to have sex with him if he did.  
• Daniel and Allison continued having sexual intercourse.  
• Allison has recently discovered that she contracted syphilis from Daniel.  
• Allison would not have continued having sex with Daniel had she known he had 
syphilis. 
"""
    case_file_names = ['2012_2RCS_584.pdf', '1990canlii95.pdf', '2017nbca10.pdf', 'Cowan-en.pdf', 'Khill-en.pdf']
    #commands(index_name, embeddings)
    #print(issue_spot(factsheet))
    #print(evaluate_relevancy(sample_fact_sheet, index_name, embeddings, name_space='criminal_law'))
    #print(list_all_embeddings(pinecone_index))
    meta_filter = {'source': case_file_names[3]}
    index = get_existing_index(index_name, embeddings, 'criminal_law')
    print(evaluate_relevancy(sample_fact_sheet, index, meta_filter)['answer'])

if __name__ == '__main__':
    main()
