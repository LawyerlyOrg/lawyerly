import pytest
import pymongo
from db import *

@pytest.fixture
def file_name():
    file_name = '2012_2RCS_584.pdf'
    return file_name

@pytest.fixture
def sample_summary():
    sample_summary = """The defendant is accused of failing to disclose his HIV-positive status to nine complainants before having sex with them, which did not result in any of the complainants contracting HIV. The actus reus of the charged crime is failing to disclose one's HIV-positive status to a sexual partner before having sex with them, and the mens rea is intent to deceive."""
    return sample_summary

def test_insert_multiple_collections_one_user():
    user_email = "gary.smith@gmail.com"
    first_name = "Gary"
    last_name = "Smith"
    
    # Step 1: create a new user
    user_id = insert_new_user(user_email, first_name, last_name)


def test_db_insert_operations(file_name, sample_summary):
    user_email = "gary.smith@gmail.com"
    first_name = "Gary"
    last_name = "Smith"
    
    # Step 1: create a new user
    user_id = insert_new_user(user_email, first_name, last_name)

    # Step 2: create a collection for the user
    collection_name = "Frank's Case"
    collection_description = "Frank's troublesome history with passing on STD's"
    collection_id = insert_new_collection(user_email, collection_name, collection_description)

    # Fetch collection_ids to check
    user_object = user_col.find_one({'_id':user_email})
    collection_ids = user_object['collection_ids']

    assert collection_id in collection_ids
    #that collection id is in user array

    # Step 3: create a new document(s) to populate the collection
    case_summary_id = insert_new_case_summary(collection_id, file_name, sample_summary)

    # Fetch case_summary_ids to check
    collection_object = collection_col.find_one({'_id':collection_id})
    case_summary_ids = collection_object['case_summary_ids']

    assert case_summary_id in case_summary_ids
