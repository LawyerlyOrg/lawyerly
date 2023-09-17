import sys
import os.path
import os
from io import BytesIO
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from flask import Flask, request, jsonify
from flask_restx import reqparse
from gpt_search import chat_with_index, get_existing_index
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import openai
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from db import get_user_collections, insert_new_collection, insert_new_fact_sheet, get_collection_name, get_fact_sheets, get_case_summary_ids
from evaluate_cases import evaluate_relevancy_for_summaries_in_collection
from ingest import pdf_to_string, process_pdfs
from bson.objectid import ObjectId
from bson.errors import InvalidId
from install_certificates import handle_certificates

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

with app.app_context():
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
        openai.api_key = os.environ["OPENAI_API_KEY"]
        pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment="northamerica-northeast1-gcp"
        )
        index_name = "test4"

# TODO: in the future, make a chat function, whereby user can query their private data.
# use combination of user_email and collection_name to create a name_space for pinecone.
# optional to chat with all documents in the collection or a specified file.
@app.route('user/<string:user_email>/collection/<string:collection_id>/chat_with_index', methods=['GET'])
def chat(user_email, collection_id):
    query = request.args.get('prompt')
    print('query', query)
    collection_name = get_collection_name(ObjectId(collection_id)) 
    index = get_existing_index(index_name, embeddings, collection_name)
    text = chat_with_index(query, index)['answer']
    return text, 200

@app.route('/collection/<string:collection_id>/factsheets', methods=['POST', 'GET'])
def factsheets(collection_id):

    if request.method == "POST":
        pdf_files = {}
        ids = []

        # Check that upload is not empty
        if len(request.files) == 0:
            return "No files uploaded", 400

        for key in request.files:
            try:
                current_file = request.files.get(key)
                filename = current_file.filename
                file = current_file.read()
                stream = BytesIO(file)
                string = pdf_to_string(stream)
            except PdfReadError:
                return "Invalid file type", 400
            else:
                pdf_files[filename] = string

        # Create fact sheet(s)
        for file_name, fact_string in pdf_files.items():
            ids.append(str(insert_new_fact_sheet(ObjectId(collection_id), file_name, fact_string)))

        return jsonify(ids), 201
    
    if request.method == "GET":
        fact_sheet_ids = get_fact_sheets(ObjectId(collection_id))
        return fact_sheet_ids, 200

@app.route('/user/<string:user_email>/collections', methods=['POST', 'GET'])
def collections(user_email):

    if request.method == 'GET':

        data = get_user_collections(user_email=user_email)

        return jsonify(data), 200

    if request.method == 'POST':
       
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="Collection Name cannot be blank!")
        parser.add_argument("description", required=True, help="Collection Description cannot be blank!")
        args = parser.parse_args()
    
        collection_name = args["name"]
        collection_description = args["description"]
    
        print(f'user email: {user_email}')
        print(f'collection name: {collection_name}')
        print(f'collection description: {collection_description}')
    
        collection_id = str(insert_new_collection(user_email, collection_name, collection_description))
    
        return collection_id, 201

# TODO: update so that when processing PDFs, pass in collection_name and user_email, so that can
# be utilized to create the namespace within pinecone index.
@app.route('/collection/<string:collection_id>/cases',  methods=['POST', 'GET'])
def cases(collection_id):
    
    if request.method == "POST":

        # Check if collection exists by fetching name
        try:
            collection_name = get_collection_name(ObjectId(collection_id))
            print(f'collection name: {collection_name}')
        except InvalidId:
            return "Invalid collection id", 400


        parser = reqparse.RequestParser()
        parser.add_argument("law_area", required=True, help="Law area cannot be blank!")
        args = parser.parse_args()
        
        law_area = args["law_area"]

        if len(request.files) == 0:
            return "No files uploaded", 400

        for key in request.files:
            try:
                current_file = request.files.get(key)
                PdfReader(current_file)
            except PdfReadError:
                return "Invalid file type", 400
            
        process_pdfs(request.files, embeddings, index_name, collection_name, ObjectId(collection_id), law_area, api_mode=True)

        return 'Case file(s) summarized successfully', 201

    if request.method == 'GET':
        case_summary_ids = get_case_summary_ids(ObjectId(collection_id))
        return case_summary_ids, 200

@app.route('/relevancies',  methods=['GET'])
def relevancies(): 

    parser = reqparse.RequestParser()
    parser.add_argument("collection_id", required=True, type=str, help="Collection id cannot be blank!")
    parser.add_argument("fact_sheet_id", required=True, type=str, help="Fact sheet id cannot be blank!")
    args = parser.parse_args()

    collection_id = args["collection_id"]
    fact_sheet_id = args["fact_sheet_id"]
    
    relevancies = evaluate_relevancy_for_summaries_in_collection(ObjectId(collection_id), ObjectId(fact_sheet_id))

    return jsonify(relevancies), 200

@app.route('/')
def home():
    return 'Home Page Route'

if __name__ == '__main__':
    handle_certificates()
    app.run()