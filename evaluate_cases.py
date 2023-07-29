import openai
from search import *

# including the set of vectors that correspond to each case - 

def evaluate_relevancy(fact_sheet, index, meta_filter):

    # query = f"""
    # What are common themes between the document and the fact sheet delimited by triple backticks?  

    # Legal fact sheet: ```{fact_sheet}```
    # """

    # query = f"""
    # What are the similarities between the document and the fact sheet delimited by triple backticks?

    # Legal fact sheet: ```{fact_sheet}```
    # """

    query = f"""
   
    Task 1: Describe what the defendant is accused of in the Document.

    Task 2: Describe the actions and circumstances of the defendant in the Document.

    Task 3: Describe the effect of the defendant's actions on the victim in the Document.

    Task 4: Describe the actus reus of the charged crime. Respond "I do not know" if you do not know.

    Task 5: Describe the mens rea of the charged crime. Respond "I do not know" if you do not know.

    Task 6: Describe the specific legal framework used to determine the defendant's criminal liability.

    """

    # query = f"""

    # Please describe the specific rule, test, or framework used evaluate criminal liability in the document.

    # Please describe how the defendant's conduct is evaluated by the rule, test, or framework in the document.

    # Please reference any relevant criminal code provisions, statutes, or other criminal cases when describing the rule.

    # """

    #query = f"""In bullet point form, what are the similarities between the document and the fact sheet delimited by triple backticks? Legal fact sheet: ```{fact_sheet}```"""


    return search(query, index, meta_filter)

