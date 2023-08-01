import openai
from gpt_search import *

def evaluate_relevancy(summary_string, fact_sheet):

    prompt = f"""
   
    Find the similarities between the Summary and the Factsheet in bullet point form.
    Summary: ```{summary_string}```
    Factsheet: ```{fact_sheet}```
    """
    
    return get_completion(prompt)


def extract_summary(index, meta_filter):

    query = f"""
    Step 1: Describe what the defendant is accused of in the Document.
    Step 2: Describe the actions and circumstances of the defendant in the Document.
    Step 3: Describe the effect of the defendant's actions on the victim in the Document.
    Step 4: Describe the actus reus of the charged crime. Respond "I do not know" if you do not know.
    Step 5: Describe the mens rea of the charged crime. Respond "I do not know" if you do not know.
    """

    return search(query, index, meta_filter)['answer']
