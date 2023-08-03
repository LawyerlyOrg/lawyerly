from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongo