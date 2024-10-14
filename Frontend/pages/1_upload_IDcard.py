import io
import streamlit as st
from io import StringIO
from PIL import Image


st.title("Upload your ID-card image :")

#  it’s always going to return a BytesIO object.
IDcard_image = st.file_uploader("select an image : ")


if IDcard_image is not None :

    image_to_bytes = IDcard_image.getvalue()

    image = Image.open(IDcard_image)
    st.image(image )
    #st.write(image_to_bytes)

st.write(" ")



st.markdown(
    """
    <style>
    .white-bold-text {
        color: #FAFAFA;
        font-family: 'Thaoma', monospace;
        font-size: 25px;
        font-weight: bold;
        text-decoration: none;  /* Removes underline */
        display: flex;
        justify-content: center;
        align-items: center;
        text-align: center;
        border: 1px solid #262730; 
        border-radius: 6px;  
        padding: 10px;  
        background-color: #262735;
        width: 24%;  
        margin: 0 auto; 
    }
    </style>
    """,
    unsafe_allow_html=True
)
#st.page_link("pages/2_take_picture.py", label='Next Stage ⏭', use_container_width=True  )


#st.link_button("Next Stage ⏭", "take_picture")


st.markdown('<a href="take_picture" target="_self" class="white-bold-text">Next Stage</a>', unsafe_allow_html=True )
