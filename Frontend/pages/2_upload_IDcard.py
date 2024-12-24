import streamlit as st
from PIL import Image
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from AI_FaceVerificatin.face_verification import faceExtraction

st.title("Upload your ID-card image :")

IDcard_image = st.file_uploader("select an image : ")

if IDcard_image is not None :

    image_to_bytes = IDcard_image.getvalue()

    image = Image.open(IDcard_image)
    image.save("./output/idcard.jpg")
    st.image(image)
    faceExtraction("../Frontend/output/idcard.jpg" , "idcard")

st.write(" ")
st.markdown("""<style>.white-bold-text {color: #FAFAFA;font-family: 'Thaoma', monospace;font-size: 25px;font-weight: bold;
        text-decoration: none; display: flex;
        justify-content: center;align-items: center;
        border: 1px solid #262730; 
        border-radius: 6px;  padding: 10px;  
        background-color: #262735;width: 24%;  }</style>""",
    unsafe_allow_html=True)

st.markdown('<a href="take_picture" target="_self" class="white-bold-text">Next Step</a>', unsafe_allow_html=True )

#st.page_link("pages/2_take_picture.py", label='Next Step', use_container_width=True  )
#st.link_button("Next Stage ⏭", "take_picture")

