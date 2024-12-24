import sys
from fastapi import FastAPI , UploadFile , HTTPException , Header  , Depends
import json 
sys.path.append('../AI_FaceVerificatin')
from celery_tasks import celery_app , face_task , speech_task , hand_gesture_task
from pydantic import BaseModel , EmailStr 
from passlib.context import CryptContext
import jwt
from database import User
import datetime as datetime
from datetime import timedelta

app = FastAPI()

# hashing passwords
# for saving passwords in database , we must hash them first ,and then save them in DB
pwd_context = CryptContext(schemes=["bcrypt"] , deprecated="auto")

#checking data's validation
class SignUpRequest(BaseModel):
    email: EmailStr
    password: str

class SignInRequest(BaseModel):
    email: EmailStr
    password: str

# از طریق ای پی آی قراره توکن برای ما ارسال بشه
# when api wants to return that Token , as a response , it will return with this structure :
class TokenResponse(BaseModel):
    access_token : str
    token_type : str

# A function for converting password --> into hashed password
def get_hashed_password(password: str) -> str :
    return pwd_context.hash(password)


# A function that compares "signin password" with "login password which is being hashed" , and do the verification task
def verify_password(plain_password:str , hashed_password:str) -> bool:
    return pwd_context.verify(plain_password , hashed_password)


# convert email to token
def create_accesss_token(email_data: dict) -> str :
    to_encode = email_data.copy()
    # each token will be expire after 30 minutes 
    expire = datetime.datetime.now(datetime.timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp":expire})
    token = jwt.encode(to_encode , "secret-key" , algorithm="HS256")
    return token


# convert token to email
def decode_access_token(token: str):
    # decoding email 
    try :
        payload = jwt.decode( token , "secret-key" , algoritms=["HS256"])
        return payload.get("email")
    except jwt.ExpiredSignatureError :
        raise HTTPException(status_code=408 , detail="Token has expired")
    except jwt.InvalidTokenError :
        raise HTTPException(status_code=406 , detail="Invalid token")



def get_current_user(authorization: str = Header(None)) -> str :
    # it will extract current user from authorization
    # we are hashing 2 things :
    # 1_ password  , 
    # 2_ email : we are also hashing email , & call it TOKEN
    # we recieve this TOKEN , then we decode it with (decode_access_token) 
    # now we have email , so we search database and find user related to that email .
    if not authorization  or  not authorization.startswith("Bearer ") :
        raise HTTPException(status_code=401 , detail="Missing or invalid authorization header")
    token = authorization.split(" ")[1]
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=406 , detail="Invalid token")
    return email



@app.get("/")
async def root():
    x = json.loads('{"respond" :"Hello world !"}')
    return x["respond"]


@app.post("/signup" , status_code=201)
def signup(request:SignUpRequest):
    if User.objects(email=request.email).first():
        raise HTTPException(status_code=400 , detail="Email already registered")
    hashed_password = get_hashed_password(request.password)
    # create new object from User class (in database file)
    User(email=request.email  , hashed_password=hashed_password , user_level=1).save() # save == INSERT INTO table
    return {"message" : "user registered successfully."}


# this func , is going to create token , and then return that access token
@app.post("/signin" , response_model=TokenResponse)
def signin(request: SignInRequest):
    user = User.objects(email=request.email).first()
    if not user or not verify_password(request.password  , user.hashed_password):
        raise HTTPException(status_code=401 , detail="invalid email or password")
    # if user exists :
    access_token = create_accesss_token(email_data={"email":user.email})
    return {"access_token":access_token , "token_type":"Bearer"}


@app.get("/notprotected") # for using t his api user doesnt need to any access token
def test1():
    return {"message":"Hello everyone"}


@app.get("/protected") # only users with access token can call this api
def test2(current_user:str=Depends(get_current_user)):
    return {
        "message": f"Hello {current_user} you have access to this route "
    }

@app.post("/signout")
def signout(token: str = Depends(decode_access_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return {"message": "Sign-out successful."}



# @app.get("/ekyc/face")
# async def face():
#     idcard_face = "./AI_FaceVerificatin/cropped_images/idcard_croped_face.jpg" 
#     selfie_face = "./AI_FaceVerificatin/cropped_images/selfie_croped_face.jpg"
#     faceSimilarity(idCard_face_path=idcard_face , selfie_face_path=selfie_face)
#     return {"message":"user verified ✅"}



@app.post("/ekyc/face2")
async def face2(image:UploadFile , current_user: str=Depends(get_current_user)):
    if current_user :
        image = await image.read() # output of read function is bytes like
        task = face_task.delay(image) # this output will be generated instantly , without delay . but in face_task function , outputs will return after delay
        return {
            "task_id":task.id ,
            "status":task.state }
    else :
        return {"Error":" You have not signed in yet ❌"}


@app.post("/ekyc/speech")
async def speech(voice:UploadFile , current_user: str=Depends(get_current_user)):
    if current_user :
        voice = await voice.read()
        task = speech_task.delay(voice)
        return {
            "task_id":task.id ,
            "status":task.state }
    else:
        return {"Error":" You have not signed in yet ❌"}

@app.post("/ekyc/gesture")
async def gesture(image:UploadFile , current_user: str=Depends(get_current_user)):
    if current_user :
        image = await image.read()
        task = hand_gesture_task.delay(image)
        return {
            "task_id":task.id ,
            "status":task.state }
    else:
        return {"Error":" You have not signed in yet ❌"}

# check tasks in celery
@app.get("/check_task")
def task_check(task_id:str):
    result = celery_app.AsyncResult(task_id)
    return {"status":result.status,
            "result": result.result }

# uvicorn Backend.main:app --reload --host 127.0.0.1 --port 8000