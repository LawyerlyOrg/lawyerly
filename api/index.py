import sys
import os.path
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from flask import Flask, request, jsonify
from gpt_search import chat_with_gpt
import openai
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from pymongo import MongoClient
from db import get_user_collections

app = Flask(__name__)

with app.app_context():
        #embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
        openai.api_key = os.environ["OPENAI_API_KEY"]
        #pinecone.init(
        #api_key=os.environ["PINECONE_API_KEY"],
        #environment="northamerica-northeast1-gcp"
        #)

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

@app.route('/users/<user_id>/collections', methods=['GET'])
def get_collections(user_id):
    # query the database for the collections that belong to the user
    data = get_user_collections(user_email=user_id)
    # return a JSON response with the data and status code 200
    return jsonify(data), 200

@app.route('/users/<user_id>/collections', methods=['POST'])
def create_collection(user_id):

  
    # return a success message and the collection id and status code 201
    return {'message': 'Collection created successfully'}, 201

@app.route('/upload_factsheet/<string:user_email>')
def upload_factsheet():
    print("upload factsheet")

@app.route('/upload_case_files/<string:user_email>')
def upload_casefile():
    print("upload casefile")

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