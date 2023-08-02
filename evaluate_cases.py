from gpt_search import *
import prompts

def evaluate_relevancy(summary_string, fact_sheet):

    prompt = f"""
    Find the similarities between the Summary and the Factsheet in bullet point form.
    Summary: ```{summary_string}```
    Factsheet: ```{fact_sheet}```
    """
    
    return chat_with_gpt(prompt)