import sys
import os.path
import os
from io import BytesIO
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import reqparse
from gpt_search import chat_with_gpt
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import openai
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from pymongo import MongoClient
from db import get_user_collections, insert_new_collection, insert_new_fact_sheet, get_collection_name, get_fact_sheets, get_case_summary_ids, get_case_summary,get_fact_sheet
from evaluate_cases import evaluate_relevancy_for_summaries_in_collection
from ingest import pdf_to_string, process_pdfs
from bson.objectid import ObjectId
from bson.errors import InvalidId
from bson import json_util
#from install_certificates import handle_certificates
import shutil

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

with app.app_context():
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
        openai.api_key = os.environ["OPENAI_API_KEY"]
        pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment="northamerica-northeast1-gcp"
        )
        index_name = "test4"

@app.route('/chat_with_gpt')
def chat():
    # http://10.1.1.1:5000/chat_with_gpt?prompt=what is the meaning of life?
    prompt= request.args.get('prompt')
    print('prompt', prompt)
    text = chat_with_gpt(prompt)
    return text

@app.route('/collection/<string:collection_id>/factsheets', methods=['POST', 'GET'])
def factsheets(collection_id):

    if request.method == "POST":
        pdf_files = {} # filename: string
        ids = []

        # check that upload is not empty
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
        # TODO: bulk insert to mongodb should be implemented
        for file_name, fact_string in pdf_files.items():
            ids.append(str(insert_new_fact_sheet(ObjectId(collection_id), file_name, fact_string)))

        return jsonify(ids), 201
    
    if request.method == "GET":
        fact_sheet_ids = get_fact_sheets(ObjectId(collection_id))
        fact_sheet_objects = [get_fact_sheet(ObjectId(fact_sheet_id)) for fact_sheet_id in fact_sheet_ids]
        return json_util.dumps(fact_sheet_objects), 200

@app.route('/user/<string:user_email>/collections', methods=['GET'])
def get_collections(user_email):

    # query the database for the collections that belong to the user
    data = get_user_collections(user_email=user_email)
    #print(f'data:{data}')
    # return a JSON response with the data and status code 200
    return jsonify(data), 200

@app.route('/user/<string:user_email>/collections', methods=['POST'])
def create_collection(user_email):
    # http://10.1.1.1:5000/users/user_email/collections?name=Haji's Case

    # create a parser object
    parser = reqparse.RequestParser()
    # add name and description arguments
    parser.add_argument("name", required=True, help="Collection Name cannot be blank!", location='args')
    parser.add_argument("description", required=True, help="Collection Description cannot be blank!", location='args')
    # parse the arguments from the request
    args = parser.parse_args()

    collection_name = args["name"]
    collection_description = args["description"]

    print(f'user email: {user_email}')
    print(f'collection name: {collection_name}')
    print(f'collection description: {collection_description}')

    insert_new_collection(user_email, collection_name, collection_description)

    # return a success message and the collection id and status code 201
    return {'message': 'Collection created successfully'}, 201

@app.route('/collection/<string:collection_id>/cases',  methods=['POST', 'GET'])
def cases(collection_id):
    
    if request.method == "POST":

        # check if collection exists by fetching name
        try:
            collection_name = get_collection_name(ObjectId(collection_id))
            print(f'collection name: {collection_name}')
        except InvalidId:
            return "Invalid collection id", 400

        # create a parser object
        parser = reqparse.RequestParser()
        # add name and description arguments
        parser.add_argument("law_area", required=True, help="Law area cannot be blank!", location='args')
        # parse the arguments from the request
        args = parser.parse_args()
        law_area = args["law_area"]

        # check that upload is not empty
        if len(request.files) == 0:
            return "No files uploaded", 400

        # check that all files are valid PDF
        for key in request.files:
            try:
                current_file = request.files.get(key)
                PdfReader(current_file)
            except PdfReadError:
                return "Invalid file type", 400
            
        # process step
        process_pdfs(request.files, embeddings, index_name, collection_name, ObjectId(collection_id), law_area, api_mode=True)

        return {'message': 'Case file(s) summarized successfully'}, 201

    if request.method == 'GET':
        case_summary_ids = get_case_summary_ids(ObjectId(collection_id))
        case_objects = [get_case_summary(ObjectId(case_summary_id)) for case_summary_id in case_summary_ids]
        return json_util.dumps(case_objects), 200

@app.route('/relevancies',  methods=['GET'])
def relevancies(): #/relevancies?collection_id=00000000000000&fact_sheet_id=0101010101001
    # create a parser object
    # args = request.args.to_dict()
    parser = reqparse.RequestParser()
    # add name and description arguments
    parser.add_argument("collection_id", required=True, type=str, help="Collection id cannot be blank!", location='args')
    parser.add_argument("fact_sheet_id", required=True, type=str, help="Fact sheet id cannot be blank!", location='args')
    # parse the arguments from the request
    print("line 178")
    args = parser.parse_args()
    print("line 180")
    collection_id = args["collection_id"]
    fact_sheet_id = args["fact_sheet_id"]
    relevancies = evaluate_relevancy_for_summaries_in_collection(ObjectId(collection_id), ObjectId(fact_sheet_id))
    #print('Case file(s) evaluated for relevancy against fact sheet successfully!')
    #print(relevancies, type(relevancies))
    return jsonify(relevancies), 200

@app.route('/')
def root():
    return 'Home Page Route'

@app.route('/about')
def about():
    return 'About Page Route'

@app.route('/portfolio')
def portfolio():
    return 'Portfolio Page Route'

@app.route('/contact')
def contact():
    return 'Contact Page Route'

if __name__ == '__main__':
   
    #handle_certificates()
    app.run()