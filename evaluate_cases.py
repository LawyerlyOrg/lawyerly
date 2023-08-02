from gpt_search import *
import prompts

def extract_summary(law_area, index, meta_filter):
    query = prompts.prompt_dict[law_area]

    return search(query, index, meta_filter)['answer']

def evaluate_relevancy(summary_string, fact_sheet):

    prompt = f"""
    Find the similarities between the Summary and the Factsheet in bullet point form.
    Summary: ```{summary_string}```
    Factsheet: ```{fact_sheet}```
    """
    
    return get_completion(prompt)