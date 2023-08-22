from gpt_search import *
import prompts
from db import get_case_summary_ids, get_case_summary, get_fact_sheet
from bson.objectid import ObjectId

def evaluate_relevancy(summary_string, fact_sheet):

    prompt = f"""
    Find the similarities between the Summary and the Factsheet in bullet point form.
    Summary: ```{summary_string}```
    Factsheet: ```{fact_sheet}```
    """
    
    return chat_with_gpt(prompt)

def evaluate_relevancy_for_summaries_in_collection(collection_id, fact_sheet_id):

    relevancies = {} # case_summary_id : relevancy
    summaries = get_case_summary_ids(collection_id)
    fact_sheet = get_fact_sheet(fact_sheet_id)
    for summary_id in summaries:
        summary_string = get_case_summary(summary_id)["summary"]
        relevancies[summary_id] = evaluate_relevancy(summary_string, fact_sheet)
    
    return relevancies


