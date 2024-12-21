# eKYC Backend :

# How to run :

+ in windows , Docker desktop needs to be open while using from docker containers.

<br>

## 1_ run REDIS docker container  <br>
open a new terminal :
redis is dependent on celery for running.

```
cd Backend
# first time :
docker pull redis 
docker run --name redis-ekyc -d -p 6379:6379 redis

# other times , only need to start/run container  :
docker start redis-ekyc 
```

##  2_ Run CELERY tasks <br>

open another terminal :

```
cd Backend
celery -A celery_tasks worker --loglevel=ERROR 

or :
celery -A celery_tasks worker --pool=solo -l info --concurrency=1
```

<b> ** before runnig celery we should run redis. <b> <br>
<b> ** fastapi is also related and dependent to celery. <b>

<br>

## 3_ Run MongoDB container :
Because fastapi uses database file , we have to run this container before running main file. 
```
docker pull mongo

docker run --name mongo-ekyc -d -p 27017:27017 mongo

```


## 4_ Run main API <br>
in another terminal :
```
cd Backend

fastapi run main.py
or :
uvicorn main:app --reload --host 127.0.0.1 --port 8000

```

<br>
<br>

## 5_ open a new terminal for Gesture API :

```
cd AI_HandGesture
uvicorn app:app --reload --host 127.0.0.1 --port 8080

```

## until now, we have opened 4 terminals :
### 1_ redis
### 2_ celery
### 3_ fastapi (main)
### 4_ Gesture API


<br>




# Explanation 

+ we are going to connect fastapi(main.py) to celery. <br>
fastapi will send tasks(face/hand/audio) into celery . <br>
we are using celery because we have tasks which takes longer than others . 

+ celery is connected to redis . we will consider a same redis for broker & backend .

+ celery_tasks.py is going to make connection with another api (http://127.0.0.1:8080/ekyc/hand_gesture)

+ user only has access to (main.py) in backend.

main module is sending a request to celery , <br>
and celery is sending a request to *Gesture API* , so this gesture API is going to send back a random answer to celery .<br>

we cant call gesture api directly , instead we only need to call main API .

## ```  main.py  --->  celery_tasks.py  --->  app.py(HandGesture folder)  ```

# test in postman :
```
POST : http://127.0.0.1:8000/ekyc/gesture  
body --> image = upload image gesture file 

GET : http://127.0.0.1:8000/check_task
param --> task_id = aa49d184-0adb-4df6-a349-399925177f13

------------------------------- 

POST : http://127.0.0.1:8080/ekyc/hand_gesture
body --> form-data --> key=input_image : value = uploadimage

```


+ user is only working with main.py in Backend .  


+ why we should use a database (like MongoDB), while using redis ? 
    we are going to save user's registeration info (username-password-email-phone number & ... ) in MongoDB .
    we want to save temporary data in redis .

    <br>

    + we can create our MongoDB in : cloud.mongodb.com
    But we use the docker of MongoDB instead . because using above site needs vpn which causes slow connection . <br>
    
        ```
        docker pull mongo

        docker run --name mongo-ekyc -d -p 27017:27017 mongo
        ```

        we want to create 3 connection between main file and mongo database :
        + 1_ signup 
        + 2_ signin 
        + 3_ signout
        ## we have used mongoengine , which is an ODM
+ Here , user is sending request for main api(in backend) ;
    and main api is sending request to secondary api(hand gesture)

<br>

## pyjwt :

+ for verification and checking authenticity of user's data , we have used PYDANTIC . <br>
some of apis need authentication , so we have to use their given token like this :
```
Authorization: Bearer API-key

```
for example when we signed up , a token will be sent back into the main.py . therfore for sending EVERY requests in our application we will need THIS TOKEN . <br>
for authrizing informations we have used "Jose" or "pyjwt" libraries . <br>
"pyjwt" will ENCODE the data , and then gives us a TOKEN . <br>


## user  -->  main api   --> secondary api (hand gesture )


