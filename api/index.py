import sys
import os.path
import os
from io import BytesIO
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, reqparse
from gpt_search import chat_with_gpt
from pypdf import PdfReader
from pypdf.errors import PdfReadError
import openai
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from pymongo import MongoClient
from db import get_user_collections, insert_new_collection, insert_new_fact_sheet, get_collection_name
from ingest import pdf_to_string, process_pdfs
from bson.objectid import ObjectId
from bson.errors import InvalidId
from install_certificates import handle_certificates
import shutil


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = 'static/case_pdfs'

with app.app_context():
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
        openai.api_key = os.environ["OPENAI_API_KEY"]
        pinecone.init(
        api_key=os.environ["PINECONE_API_KEY"],
        environment="northamerica-northeast1-gcp"
        )
        index_name = "test4"

"""
class InputError(Exception):
    # custom exception class for invalid input
    def __init__(self, message):
        self.message = message
        self.status = status.HTTP_400_BAD_REQUEST

@app.errorhandler(InputError)
def handle_input_error(e):
    # error handler for input error
    return {'message': e.message, 'status': e.status}
"""

@app.route('/chat_with_gpt')
def chat():
    # http://10.1.1.1:5000/chat_with_gpt?prompt=what is the meaning of life?
    prompt= request.args.get('prompt')
    print('prompt', prompt)
    text = chat_with_gpt(prompt)
    return text

@app.route('/collection/<string:collection_id>/factsheet', methods=['POST'])
def create_factsheet(collection_id):

    pdf_files = {} # filename: string

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
        insert_new_fact_sheet(ObjectId(collection_id), file_name, fact_string)

    return "Fact sheet(s) created successfully", 200

@app.route('/user/<string:user_email>/collections', methods=['GET'])
def get_collections(user_email):

    # query the database for the collections that belong to the user
    data = get_user_collections(user_email=user_email)
    print(f'data:{data}')
    # return a JSON response with the data and status code 200
    return jsonify(data), 200

@app.route('/user/<string:user_email>/collections', methods=['POST'])
def create_collection(user_email):
    # http://10.1.1.1:5000/users/user_email/collections?name=Haji's Case

    # create a parser object
    parser = reqparse.RequestParser()
    # add name and description arguments
    parser.add_argument("name", required=True, help="Collection Name cannot be blank!")
    parser.add_argument("description", required=True, help="Collection Description cannot be blank!")
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
def ingest_case_files(collection_id):
    
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
        parser.add_argument("law_area", required=True, help="Law area cannot be blank!")
        # parse the arguments from the request
        args = parser.parse_args()
        law_area = args["law_area"]
        
        # create temp folder for ingest operations
        upload_folder = app.config['UPLOAD_FOLDER'] + '/' + collection_id
        if os.path.isdir(upload_folder):
            shutil.rmtree(upload_folder)
        os.makedirs(upload_folder) 

        # check that upload is not empty
        if len(request.files) == 0:
            return "No files uploaded", 400

        for key in request.files:
            try:
                current_file = request.files.get(key)
                filename = current_file.filename

                 # copy request files into local directory
                current_file.save(upload_folder + '/' + filename)

                # check that all files are valid PDF
                PdfReader(current_file)
            except IOError:
                return f"Could not save file: {filename}", 400
            except PdfReadError:
                return "Invalid file type", 400
            
        process_pdfs(upload_folder, embeddings, index_name, collection_name, ObjectId(collection_id), law_area)

        return {'message': 'Case file(s) summarized successfully'}, 201

@app.route('/upload_relevancy/<string:user_email>/<string:collection_id>/<string:case_id>')

@app.route('/')
def home():
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