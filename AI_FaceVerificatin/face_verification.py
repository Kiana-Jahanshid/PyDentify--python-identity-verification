import cv2.data
from deepface import DeepFace
import cv2
import numpy as np


# ectract face from id-card and selfie picture 
def faceExtraction(image_path , task):
    image = cv2.imread(image_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml' )
    faces = face_cascade.detectMultiScale(image , 1.3 , 6)
    cropped = []
    for (x,y,w,h) in faces :
        face = image[y:y+h , x:x+w]
        cropped_face = face
    cv2.imwrite(filename=f"../AI_FaceVerificatin/cropped_images/{task}_croped_face.jpg" , img=cropped_face)

def faceSimilarity(idCard_face , selfie_face):

    res = DeepFace.verify(img1_path="./AI_FaceVerificatin/cropped_images/idcard_croped_face.jpg" , img2_path="./AI_FaceVerificatin/cropped_images/selfie_croped_face.jpg" , model_name="Facenet512")
    print(res["distance"])
    if res["distance"] < 0.5 :
        return "Verified"
    else:
        return "Not Verified"


