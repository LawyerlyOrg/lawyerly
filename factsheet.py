import openai
from PyPDF2 import PdfReader

# Step 1: convert fact sheet PDF into string
def pdf_to_string(pdf_file_path):
    pdf_text = ""
    pdf_reader = PdfReader(pdf_file_path)

    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

    factsheet = pdf_text

# Step 2: issue spot and extract search terms
def issue_spot(fact_sheet):

    prompt = f"""
    Your task is to help a lawyer search for relevant cases in a legal database given a fact sheet about their client.

    Provide a list of search terms based on the information provided in the legal fact sheet delimited by triple backticks.

    Make sure the search terms are relevant to the fact sheet and are centered on the area of law identified in the fact sheet.

    Only provide up to the top 6 most relevant search terms.

    Legal fact sheet: ```{fact_sheet}```
    """

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )

    return response.choices[0].message.content