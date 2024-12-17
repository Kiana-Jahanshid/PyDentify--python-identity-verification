import io
from fastapi import FastAPI , UploadFile , File
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision 
from PIL import Image


#_________________ gesture recognition api ________________#

app = FastAPI()

@app.get("/")
def root():
    return {"message":"this is a Gesture API"}


@app.post("/ekyc/hand_gesture")
async def hand_gesture(input_image:UploadFile=File(...)):
        baseoptions = python.BaseOptions(model_asset_path="models/gesture_recognizer.task")
        options = vision.GestureRecognizerOptions(base_options=baseoptions)
        recognizer = vision.GestureRecognizer.create_from_options(options)
         

        input_image = await input_image.read() # image type is byte here , so it shoul convert to a numpy-array , then send it to mediapipe
        input_image = Image.open(io.BytesIO(input_image))
        input_image.save("result.jpg")
        image = mp.Image.create_from_file("result.jpg") # this function needs image file name , so we had to save it first 
        recognition_result = recognizer.recognize(image)
        top_gesture = recognition_result.gestures[0][0]
        #hand_landmarks = recognition_result.hand_landmarks
        return {
            "Result":top_gesture.category_name,
            "Confidence-score":top_gesture.score }