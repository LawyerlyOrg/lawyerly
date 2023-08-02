CRIMINAL_LAW_PROMPT = f"""
    Step 1: Describe what the defendant is accused of in the Document.
    Step 2: Describe the actions and circumstances of the defendant in the Document.
    Step 3: Describe the effect of the defendant's actions on the victim in the Document.
    Step 4: Describe the actus reus of the charged crime. Respond "I do not know" if you do not know.
    Step 5: Describe the mens rea of the charged crime. Respond "I do not know" if you do not know.
    """
TORT_LAW_PROMPT = ''
CONTRACT_LAW_PROMPT = ''
CONSTITUTIONAL_LAW_PROMPT = ''
ADMINISTRATIVE_LAW_PROMPT = ''
FAMILY_LAW_PROMPT = ''
IMMIGRATION_LAW_PROMPT = ''
CORPORATE_LAW_PROMPT = ''
ENVIRONMENTAL_LAW_PROMPT = ''
COPYRIGHT_LAW_PROMPT = ''
SECURITIES_LAW_PROMPT = ''
PROPERTY_LAW_PROMPT = ''

prompt_dict = {'criminal_law':CRIMINAL_LAW_PROMPT}

