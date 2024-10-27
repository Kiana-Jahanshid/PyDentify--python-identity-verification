import os
import streamlit as st
import requests
from PIL import Image
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


fastapi_url = "http://127.0.0.1:8000/ekyc"

try:
    response = requests.get(fastapi_url , proxies={'http':'','https':''})
    if response.status_code == 200:
        st.success(f"Response from FastAPI: {response.text}")
        idcard = Image.open("../AI_FaceVerificatin/cropped_images/idcard_croped_face.jpg")
        selfie = Image.open("../AI_FaceVerificatin/cropped_images/selfie_croped_face.jpg")

        col1, col2 = st.columns(2)

        # Display images side by side
        with col1:
            st.image(idcard, caption="ID-card image", use_column_width=True)

        with col2:
            st.image(selfie, caption="selfie image", use_column_width=True)
    else:
        st.error(f"Failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    st.error(f"Error: {e}")


