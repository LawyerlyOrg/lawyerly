import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

@pytest.mark.skip(reason="skiiiiiiip")
def test_insert_multiple_collections_one_user():
    user_email = "gary.smith@gmail.com"
    first_name = "Gary"
    last_name = "Smith"
    
    # Step 1: create a new user
    user_id = insert_new_user(user_email, first_name, last_name)

    # Step 2: create two collections for the user
    collection_name = "Frank's Case"
    collection_description = "Frank's troublesome history with passing on STD's"
    collection_id = insert_new_collection(user_email, collection_name, collection_description)

    # Fetch collection_ids to check
    user_object = user_col.find_one({'_id':user_email})
    collection_ids = user_object['collection_ids']

    assert collection_id in collection_ids

    collection_2_name = "Casandra's Case"
    collection_2_description = "Casandra has been creeping with Frank and now her partner wants a divorce"
    collection_2_id = insert_new_collection(user_email, collection_2_name, collection_2_description)

    # Fetch collection_ids to check
    user_object = user_col.find_one({'_id':user_email})
    collection_ids = user_object['collection_ids']

    assert collection_2_id in collection_ids

@pytest.mark.skip(reason="skiiiiiiip")
def test_insert_multiple_fact_sheets_one_collection():
    user_email = "ghaz666@gmail.com"
    first_name = "Ghazanfar"
    last_name = "Hajiabadi"
    
    # Step 1: create a new user
    user_id = insert_new_user(user_email, first_name, last_name)

    # Step 2: create two collections for the user
    collection_name = "Ghaz's Case"
    collection_description = "Ghaz's drunk accident"
    collection_id = insert_new_collection(user_email, collection_name, collection_description)

    # Step 3: create two fact sheets
    sample_fact_sheet_1 = """* Ghazanfar was drunk * Ghazanfar drove while drunk * Ghazanfar crashed"""
    file_name_1 = "Ghaz_drunk_April_2023.pdf"
    fact_sheet_1_id = insert_new_fact_sheet(collection_id, file_name_1, sample_fact_sheet_1)

    # Fetch case_summary_ids to check
    collection_object = collection_col.find_one({'_id':collection_id})
    fact_sheet_ids = collection_object['fact_sheet_ids']

    assert fact_sheet_1_id in fact_sheet_ids

    sample_fact_sheet_2 = """* Pedro is running for public office * Pedro has been approached by a private donor * Pedro was offered a donation * Pedro was asked to consider modifying govt policy"""
    file_name_2 = "Pedro_accepting_bribe_2022.pdf"
    fact_sheet_2_id = insert_new_fact_sheet(collection_id, file_name_2, sample_fact_sheet_2)
    
    collection_object = collection_col.find_one({'_id':collection_id})
    fact_sheet_ids = collection_object['fact_sheet_ids']
    
    assert fact_sheet_2_id in fact_sheet_ids

@pytest.mark.skip(reason="skiiiiiiip")
def test_insert_multiple_case_summaries_one_collection(file_name, sample_summary):
    user_email = "mohsen@gmail.com"
    first_name = "Mohsen"
    last_name = "Smithy"
    
    # Step 1: create a new user
    user_id = insert_new_user(user_email, first_name, last_name)

    # Step 2: create twi collections for the user
    collection_name = "Joe's Case"
    collection_description = "Joe's car accident"
    collection_id = insert_new_collection(user_email, collection_name, collection_description)
    
    # Step 3: create two case summaries
    case_summary_id = insert_new_case_summary(collection_id, file_name, sample_summary)
    
    # Fetch case_summary_ids to check
    collection_object = collection_col.find_one({'_id':collection_id})
    case_summary_ids = collection_object['case_summary_ids']

    assert case_summary_id in case_summary_ids

    sample_summary2 = "Joe was driving like a maniac off of the road when he found a deer stranded by its herd fellows..."
    file_name2 = "drunk_report.pdf"
    case_summary_2_id = insert_new_case_summary(collection_id, file_name2, sample_summary2)

    # Fetch case_summary_ids to check
    collection_object = collection_col.find_one({'_id':collection_id})
    case_summary_ids = collection_object['case_summary_ids']

    assert case_summary_2_id in case_summary_ids

#@pytest.mark.skip(reason="skiiiiiiip")
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

@pytest.mark.skip(reason="skiiiiiiip")
def test_get_collection_name():
    collection_id = '64dd36dc3cb105f0f0ef2602'
    expected_collection_name = "Frank's Case"
    received_collection_name = get_collection_name(ObjectId(collection_id))

    assert expected_collection_name == received_collection_name

