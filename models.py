from pymodm import MongoModel, fields, connect
from constants import *

# Establish a connection to the database.
connect(MONGODB_URI)

# these are the summaries of the cases the user will upload.
class CaseSummary(MongoModel):
	name = fields.CharField(primary_key=True)
	summary = fields.CharField()

# this is the private data (e.g. contracts, evidence, etc), and legislation that the user may want to query	
class ChatFile(MongoModel):
	name = fields.CharField(primary_key=True)
	
# these are the different client files a user has active
class Collection(MongoModel):
	name = fields.CharField(primary_key=True)
	description = fields.CharField()
	fact_sheet = fields.CharField()
	case_summaries = fields.EmbeddedDocumentListField(CaseSummary)
	chat_files = fields.EmbeddedDocumentListField(ChatFile)
	
class User(MongoModel):
	email = fields.EmailField(primary_key=True)
	first_name = fields.CharField()
	last_name = fields.CharField()
	collections = fields.EmbeddedDocumentListField(Collection)	

	class Meta:
		collection_name = 'user'
