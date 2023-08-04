from models import User, CaseSummary, ChatFile, Collection

def test(client):
    
    sample_fact_sheet = """
• Victim is Allison.  She and her partner are from Canada.  
• Allison is sexually active with her partner the defendant Daniel.  
• Daniel and Allison have been having sex for 14 months.  
• Prior to meeting Allison , Daniel discovered he had syphilis.  
• Daniel did not tell client Allison that he has syphilis , because he thought she would not agree to have sex with him if he did.  
• Daniel and Allison continued having sexual intercourse.  
• Allison has recently discovered that she contracted syphilis from Daniel.  
• Allison would not have continued having sex with Daniel had she known he had 
syphilis. 
"""
    case_summary_ids = ['2012_2RCS_584.pdf']
    chat_file_ids = ['Arguments for Euthanasia.pdf']
    
    CaseSummary('2012_2RCS_584.pdf', "The defendant is accused of failing to disclose his HIV-positive status to nine complainants before having sex with them, which did not result in any of the complainants contracting HIV. The actus reus of the charged crime is failing to disclose one's HIV-positive status to a sexual partner before having sex with them, and the mens rea is intent to deceive.").save()
    Collection("Fred Baker's File", 'Fred has been charged with being too sexy', sample_fact_sheet, case_summary_ids, chat_file_ids).save()
    User('gary.smith@gmail.com', 'Gary', 'Smith', "Fred Baker's File").save()
