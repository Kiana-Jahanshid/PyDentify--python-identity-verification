from deepface import DeepFace

def faceExtraction():
    ...


def faceSimilarity(idCard_face , selfie_face):

    res = DeepFace.verify(img1_path="di1.jpg" , img2_path="di.jpeg" , model_name="Facenet512")
    print(res["distance"])
    if res["distance"] < 0.5 :
        return "Verified"
    else:
        return "Not Verified"


