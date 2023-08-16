import pymongo
import os
from models import User, CaseSummary, ChatFile, Collection, FactSheet
from bson.objectid import ObjectId

client = pymongo.MongoClient(os.environ["MONGODB_URI"])
db = client['lawyerly']
chat_file_col = db['chat_file']
collection_col = db['collection']
user_col = db['user']
case_summary_col = db['case_summary']
fact_sheet_col = db['fact_sheet']

# Insert Operations

def insert_new_fact_sheet(collection_id, file_name, facts):
    fact_sheet_object = FactSheet(file_name, facts).save()
    fact_sheet_id = get_doc_id(fact_sheet_object)
    # Each new fact sheet must be stored in a collection
    add_fact_sheet_to_collection(collection_id, fact_sheet_id)

    return fact_sheet_id

def insert_new_case_summary(collection_id, file_name, summary):
    case_summary_object = CaseSummary(file_name, summary).save()
    case_summary_id = get_doc_id(case_summary_object)
    # Each new case summary must be stored in a collection
    add_case_summary_to_collection(collection_id, case_summary_id)
    
    return case_summary_id
    
def insert_new_chat_file(collection_id, file_name):
    chat_file_object = ChatFile(file_name).save()
    chat_file_id = get_doc_id(chat_file_object)
    # Each new chat file must be stored in a collection
    add_chat_file_to_collection(collection_id, chat_file_id)

    return chat_file_id

def insert_new_collection(user_email, name, description, fact_sheets=[], case_summary_ids=[], chat_file_ids=[]):
    collection_object = Collection(name, description, fact_sheets, case_summary_ids, chat_file_ids).save()
    collection_id = get_doc_id(collection_object)
    # Each new collection create muse be stored in a user
    add_collection_to_user(user_email, collection_id)

    return collection_id
    
def insert_new_user(user_email, first_name, last_name, collection_ids=[]):
    user_object = User(user_email, first_name, last_name, collection_ids).save()
    user_id = get_doc_id(user_object)

    return user_id

# Getter operations

def get_all_case_summaries(collection_id):
    collection = collection_col.find({"_id": collection_id})
    
    return collection

def get_all_chat_files(collection_id):
    print("all chat files retrieved")


def get_collection(collection_id):
    # may want results to be a dictionary of document type: document name
    results = [{'document type': 'document name'}]
    results.append(get_all_case_summaries(collection_id))
    results.append(get_all_chat_files(collection_id))
    return results

# Update operations (PRIVATE FUNCTIONS)

def add_collection_to_user(user_email, collection_id):
    user_col.update_one({'_id': user_email}, {'$push':{'collection_ids':collection_id}})

def add_fact_sheet_to_collection(collection_id, fact_sheet_id):
    collection_col.update_one({'_id': collection_id}, {'$push':{'fact_sheet_ids': fact_sheet_id}})
    
# this is a more explicit version of update_collection
def add_case_summary_to_collection(collection_id, case_summary_id):
    collection_col.update_one({'_id': collection_id}, {'$push':{'case_summary_ids':case_summary_id}})    

def add_chat_file_to_collection(collection_id, chat_file_id):
    collection_col.update_one({'_id': collection_id}, {'$push':{'chat_file_ids':chat_file_id}})    

# Remove operations

def remove_user(user_email):

    # first remove files related to user's collections - remove_collection_from_user should already handle this part.
    # fetch the collections, loop through remove_collection_from_user function

    # finally, remove the user itself
    print("user removed")

def remove_collection_from_user(user_email, collection_to_remove):

    #step 1: fetch the collection


    # loop through the files, call respective remove files functions (case_summaries and chat_files) related to the collection
        # fetch the files related to the collection
        # for each file, delete the file

    # then remove the collection itself
    print("collection removed")

def remove_case_summary_from_collection(collection, case_summary_id):
    print("case_summary removed")

def remove_chat_file_from_collection(collection, chat_file_id):
    print("chat_file removed")

# Helper methods

def case_summary_db_operations(user_email, collection_name, file_name, summary):
    # Save summary to case_summary
    # Fetch user
        # Fetch collection_ids given collection_name
            # Update collection given collection_id
    return 0

def get_doc_id(mongo_document):
    doc_bson = mongo_document.to_son()
    doc_id = doc_bson['_id']
    
    return doc_id

def get_user(user_email):
    user_object = user_col.find_one({'_id':user_email})

    return user_object

def get_user_collections(user_email):
    output = {}
    
    user_object = get_user(user_email)
    user_id = user_object['_id']

    collection_ids = user_object['collection_ids']

    collection_cursor = collection_col.find({'_id':{'$in':collection_ids}})

    for line in collection_cursor:
        output[str(line['_id'])] = line['name']
    
    return output

def not_test(client):
    
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
 
    
    #chat_file_object = ChatFile('Arguments for Euthanasia.pdf').save()
    #chat_file_id = get_doc_id(chat_file_object)
    #
    #case_summary_object = CaseSummary('2012_2RCS_584.pdf', "The defendant is accused of failing to disclose his HIV-positive status to nine complainants before having sex with them, which did not result in any of the complainants contracting HIV. The actus reus of the charged crime is failing to disclose one's HIV-positive status to a sexual partner before having sex with them, and the mens rea is intent to deceive.").save()
    #case_summary_id = get_doc_id(case_summary_object)
#
    #case_summary_object2 = CaseSummary("shiny_case_monir_rene.pdf", "This is a human generated summary!").save()
    #case_summary_id2 = get_doc_id(case_summary_object2)



    #existing_collection = collection_col.find_one({'_id':})

    # Collection contains chat and summary ids
    collection_object = Collection("Monir's File", 'Monir has too much  money').save()
    collection_id = get_doc_id(collection_object)
    
    ## User contains collection id
    #user_object = User('gary.smith@gmail.com', 'Gary', 'Smith', [collection_id]).save()
