from pymodm import MongoModel, fields, connect
import os

connect(os.environ["DB_URI"])

class CaseSummary(MongoModel):
	name = fields.CharField()
	summary = fields.CharField()

class ChatFile(MongoModel):
	name = fields.CharField()

class FactSheet(MongoModel):
	name = fields.CharField()
	facts = fields.CharField()
	
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
