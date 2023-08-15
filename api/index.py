import sys
import os.path
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from flask import Flask
from flask import request
from gpt_search import chat_with_gpt
import openai
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from pymongo import MongoClient

app = Flask(__name__)

with app.app_context():
        #embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])
        openai.api_key = os.environ["OPENAI_API_KEY"]
        #pinecone.init(
        #api_key=os.environ["PINECONE_API_KEY"],
        #environment="northamerica-northeast1-gcp"
        #)

@app.route('/chat_with_gpt')
def chat():
    # http://10.1.1.1:5000/chat_with_gpt?prompt=what is the meaning of life?
    prompt= request.args.get('prompt')
    print('prompt', prompt)
    text = chat_with_gpt(prompt)
    return text

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