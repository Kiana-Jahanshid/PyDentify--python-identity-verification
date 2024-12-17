import time 
from celery import Celery
import random
import json
import requests 


# read data from a single redis ---> CELERY ---> store data into that same redis
# so if we define broker == backend , means that we have a single REDIS
celery_app = Celery("tasks",
                    broker="redis://localhost:6379",    # input    
                    backend="redis://localhost:6379")   # result or output

proxies = {
    "http": None,
    "https": None,
}


@celery_app.task
def face_task(face_data: bytes):
    time.sleep(10)
    result = random.choice([True,False])
    return {
        "status":"completed",
        "result":result
    }


@celery_app.task
def speech_task(voice_data: bytes):
    time.sleep(15)
    result = random.choice([True , False])
    return {
        "status":"completed",
        "result":result
    }



@celery_app.task
def hand_gesture_task(gesture_data:bytes):
    files=[('input_image',('vic.jpg', gesture_data ,'application/octet-stream'))]
    response = requests.post("http://127.0.0.1:8080/ekyc/hand_gesture" , files=files , proxies=proxies) # its a request from celery to --> Gesture API which has 8080 port number 
    response = response.json()
    return {
        "status":"completed",
        "result":response
    }

 

# in celery data which are transsmitted are from (int/float/string/byte) type 
# here we cant use numpy-array or tensor  