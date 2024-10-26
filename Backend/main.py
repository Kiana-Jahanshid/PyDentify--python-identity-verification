from fastapi import FastAPI
import json 
from pymongo import MongoClient # pymongo connects FastAPI to MongoDB
from Celery.task import add_numbers
from AI_FaceVerificatin.face_verification import faceExtraction , faceSimilarity

app = FastAPI()

client = MongoClient("mongodb://mongodb:27017/ekyc_db")
database = client.ekyc_db


@app.get("/")
async def root():
    x = json.loads('{"respond" :"Hello world !"}')
    return x["respond"]


# mongodb
@app.get("/add_sample/")
async def addSample():
    database.users.insert_one({"name":"sarah"})
    return {"message":"user added"}


#celery 
@app.get("/add/")
def add_numbers_route(a: int, b: int):
    task = add_numbers.delay(a, b)
    return {"task_id": task.id}


@app.get("/ekyc")
async def ekyc():
    faceSimilarity(idCard_face=" " , selfie_face=" ")
    return {"message":"user verified ✅"}



# uvicorn main:app