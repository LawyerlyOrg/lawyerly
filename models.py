from pymodm import MongoModel, fields, connect
import os

# Establish a connection to the database.
connect(os.environ["DB_URI"])

# these are the summaries of the cases the user will upload.
class CaseSummary(MongoModel):
	name = fields.CharField()
	summary = fields.CharField()

# this is the private data (e.g. contracts, evidence, etc), and legislation that the user may want to query	
class ChatFile(MongoModel):
	name = fields.CharField()

class FactSheet(MongoModel):
	name = fields.CharField()
	facts = fields.CharField()
	
# these are the different client files a user has active
class Collection(MongoModel):
	name = fields.CharField()
	description = fields.CharField()
	fact_sheet_ids = fields.ListField(blank=True)
	case_summary_ids = fields.ListField(blank=True)
	chat_file_ids = fields.ListField(blank=True)
	
class User(MongoModel):
	email = fields.EmailField(primary_key=True)
	first_name = fields.CharField()
	last_name = fields.CharField()
	collection_ids = fields.ListField(blank=True)

	class Meta:
		collection_name = 'user'
