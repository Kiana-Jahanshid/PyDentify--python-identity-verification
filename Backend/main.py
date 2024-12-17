import sys
import os
from fastapi import FastAPI , UploadFile
import json 
sys.path.append('../AI_FaceVerificatin')
from celery_tasks import celery_app , face_task , speech_task , hand_gesture_task
from database import User
from pydantic import BaseModel , EmailStr


app = FastAPI()



@app.get("/")
async def root():
    x = json.loads('{"respond" :"Hello world !"}')
    return x["respond"]


# mongodb
@app.get("/add_sample/")
async def addSample():
    ...




# @app.get("/ekyc/face")
# async def face():
#     idcard_face = "./AI_FaceVerificatin/cropped_images/idcard_croped_face.jpg" 
#     selfie_face = "./AI_FaceVerificatin/cropped_images/selfie_croped_face.jpg"
#     faceSimilarity(idCard_face_path=idcard_face , selfie_face_path=selfie_face)
#     return {"message":"user verified ✅"}



@app.post("/ekyc/face2")
async def face2(image:UploadFile):
    image = await image.read() # output of read function is bytes like
    task = face_task.delay(image) # this output will be generated instantly , without delay . but in face_task function , outputs will return after delay
    return {
        "task_id":task.id ,
        "status":task.state
    }


@app.post("/ekyc/speech")
async def speech(voice:UploadFile):
    voice = await voice.read()
    task = speech_task.delay(voice)
    return {
        "task_id":task.id ,
        "status":task.state
    }


@app.post("/ekyc/gesture")
async def gesture(image:UploadFile):
    image = await image.read()
    task = hand_gesture_task.delay(image)
    return {
        "task_id":task.id ,
        "status":task.state
    }



@app.get("/check_task")
def task_check(task_id:str):
    result = celery_app.AsyncResult(task_id)
    return {"status":result.status,
            "result": result.result}

# uvicorn Backend.main:app --reload --host 127.0.0.1 --port 8000