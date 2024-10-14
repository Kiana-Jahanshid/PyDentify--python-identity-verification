from fastapi import FastAPI
import json 


app = FastAPI()

@app.get("/")
def root():
    x = json.loads('{"respond" :"Hello world !"}')
    return x["respond"]
