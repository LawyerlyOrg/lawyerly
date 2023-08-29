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

# Insert operations

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

# Get operations

def get_case_summary(case_summary_id):
    case_summary = case_summary_col.find_one({"_id": case_summary_id})
    return case_summary

def get_case_summary_ids(collection_id):
    collection_obj = collection_col.find_one({"_id": collection_id})
    case_summary_ids = collection_obj['case_summary_ids']

    output = [str(i) for i in case_summary_ids]
    
    return output

def get_collection_name(collection_id):
    collection_obj = collection_col.find_one({"_id": collection_id})
    collection_name = collection_obj['name']
    
    return collection_name

def get_fact_sheet(fact_sheet_id):
    fact_sheet = fact_sheet_col.find_one({"_id":fact_sheet_id})
    return fact_sheet

def get_user_collections(user_email):
    output = {}
    
    user_object = get_user(user_email)
    user_id = user_object['_id']

    collection_ids = user_object['collection_ids']

    collection_cursor = collection_col.find({'_id':{'$in':collection_ids}})

    for line in collection_cursor:
        output[str(line['_id'])] = line['name']
    
    return output

def get_fact_sheets(collection_id):
    collection_obj = collection_col.find_one({"_id": collection_id})
    fact_sheet_ids = collection_obj['fact_sheet_ids']

    output = [str(i) for i in fact_sheet_ids]

    return output
    
# Update operations (PRIVATE FUNCTIONS)

def add_collection_to_user(user_email, collection_id):
    user_col.update_one({'_id': user_email}, {'$push':{'collection_ids':collection_id}})

def add_fact_sheet_to_collection(collection_id, fact_sheet_id):
    collection_col.update_one({'_id': collection_id}, {'$push':{'fact_sheet_ids': fact_sheet_id}})
    
def add_case_summary_to_collection(collection_id, case_summary_id):
    collection_col.update_one({'_id': collection_id}, {'$push':{'case_summary_ids':case_summary_id}})    

def add_chat_file_to_collection(collection_id, chat_file_id):
    collection_col.update_one({'_id': collection_id}, {'$push':{'chat_file_ids':chat_file_id}})    

# Remove operations

# Helper methods

def get_doc_id(mongo_document):
    doc_bson = mongo_document.to_son()
    doc_id = doc_bson['_id']
    
    return doc_id

def get_user(user_email):
    user_object = user_col.find_one({'_id':user_email})

    return user_object


