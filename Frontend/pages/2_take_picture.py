import streamlit as st
from PIL import Image
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from AI_FaceVerificatin.face_verification import faceExtraction


st.title("Please Take a picture of yourself :")

enable = st.checkbox("Enable camera")
selfie = st.camera_input("Take a picture" , disabled= not enable)
if selfie :
    st.image(selfie)
    selfie = Image.open(selfie)
    selfie.save("./output/selfie.jpg")
    faceExtraction(image_path="./output/selfie.jpg" , task="selfie")

st.write(" ")
st.markdown("""<style>.white-bold-text {color: #FAFAFA;font-family: 'Thaoma', monospace;font-size: 25px;font-weight: bold;
        text-decoration: none; display: flex;
        justify-content: center;align-items: center;
        text-align: center;border: 1px solid #262730; 
        border-radius: 6px;  padding: 10px;  
        background-color: #262735;width: 24%;}</style>""",
    unsafe_allow_html=True)

st.markdown('<a href="record_voice" target="_self" class="white-bold-text">Next Step</a>', unsafe_allow_html=True )

#st.page_link("pages/2_take_picture.py", label='Next Stage ⏭', use_container_width=True  )
#st.link_button("Next Stage ⏭", "take_picture")

