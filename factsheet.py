import openai
from PyPDF2 import PdfReader

sample_factsheet = """ 
- Client is Allison. She and her partner are from Canada. 
- Allison is sexually active with her partner Daniel. 
- Daniel and Allison have been having sex for 14 months. 
- Prior to meeting Allison, Daniel discovered he had syphilis. 
- Daniel did not tell client Allison that he has syphilis, because he thought she would not agree to have sex with him if he did. 
- Daniel and Allison continued having sexual intercourse. 
- Allison has recently discovered that she contracted syphilis from Daniel. 
- Allison would not have continued having sex with Daniel had she known he had syphilis.
"""
factsheet = """
• Client is Allison.  She and her partner are from Canada.  
• Allison is sexually active with her partner Daniel.  
• Daniel and Allison have been having sex for 14 months.  
• Prior to meeting Allison , Daniel discovered he ha d syphilis.  
• Daniel did not tell client Allison that he has syphilis , because he thought she would not agree to have sex with him if he did.  
• Daniel and Allison continued having sexual intercourse.  
• Allison has recently discovered that she contracted syphilis from Daniel.  
• Allison would not have continued having sex with Daniel had she known he had 
syphilis. 
"""

# Step 1: convert fact sheet PDF into string
def pdf_to_string(pdf_file_path):
    pdf_text = ""
    pdf_reader = PdfReader(pdf_file_path)

    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

    factsheet = pdf_text

# Step 2: issue spot and extract search terms
def issue_spot(factsheet=factsheet):

    prompt = f"""
    Your task is to help a lawyer search for relevant cases in a legal database given a fact sheet about their client.

    Provide a list of search terms based on the information provided in the legal fact sheet delimited by triple backticks.

    Make sure the search terms are relevant to the fact sheet and are centered on the area of law identified in the fact sheet.

    Only provide up to the top 6 most relevant search terms.

    Legal fact sheet: ```{factsheet}```
    """

    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
    )

    return response.choices[0].message.content