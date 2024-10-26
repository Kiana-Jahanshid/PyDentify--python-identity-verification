import streamlit as st
import requests


fastapi_url = "http://127.0.0.1:8000/ekyc"

try:
    response = requests.get(fastapi_url , proxies={'http':'','https':''})
    if response.status_code == 200:
        st.success(f"Response from FastAPI: {response.text}")
    else:
        st.error(f"Failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    st.error(f"Error: {e}")

