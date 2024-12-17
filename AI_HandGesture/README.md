
+ if we want to run fasapi Directly , without celery , redis (just for testing): 

```
cd AI_HandGesture
uvicorn app:app --reload --host 127.0.0.1 --port 8080

in postman :

POST : http://127.0.0.1:8080/ekyc/hand_gesture
body --->  form-data  --->  key= input_image  /  value= UploadFile

```