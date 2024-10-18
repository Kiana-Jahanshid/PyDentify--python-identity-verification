from fastapi import FastAPI
import json 
from pymongo import MongoClient # pymongo connects FastAPI to MongoDB
from ..celery.task import add_numbers


app = FastAPI()

client = MongoClient("mongodb://mongodb:27017/")
database = client.ekyc_db


@app.get("/")
def root():
    x = json.loads('{"respond" :"Hello world !"}')
    return x["respond"]


# mongodb
@app.get("/add_sample/")
def addSample():
    database.users.insert_one({"name":"sarah"})
    return {"message":"user added"}


#celery 
@app.get("/add/")
def addNumbers(a,b):
    return a+b 




# uvicorn main:app