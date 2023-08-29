CRIMINAL_LAW_PROMPT = f"""
    Provide a legal summary of the Document
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

# What is the crime?
# what is the actus reus of this crime? How did the defendant's actions compare?
# What i...

"""
Using the Document, describe what the judge said about the defendant's actions and whether they were guilty of the charged crime.
Q1: Describe the crime that the defendant has been charged with.
A1: The defendant has been charged with criminal negligence causing death.

Q2: Describe the actus reus of the crime criminal negligence causing death.
A2: The actus reus of criminal negligence causing death is an act that is done with a marked and substantial departure from the standard of care that a reasonable person would have exercised in the same circumstances. It must be proven beyond a reasonable doubt that the accused's act in response to force or a threat thereof was unreasonable, with reference to all of the relevant factors listed under s. 34(2).
    
"""