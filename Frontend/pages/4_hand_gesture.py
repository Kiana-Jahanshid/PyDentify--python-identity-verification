import streamlit as st
from streamlit.components.v1 import html


st.title("Match your hand's gesture with patterns:")

#enable = st.checkbox("Enable camera")
#hand_img = st.camera_input("Bring your hand in front of camera" , disabled= not enable )

st.markdown('''

    <link href="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.css" rel="stylesheet">
    <script src="https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"></script>
    <section id="demos" class="invisible">
    <p>Use your hand to make gestures in front of the camera to get gesture classification. </br>Click <b>enable webcam</b> below and grant access to the webcam if prompted.</p>
    <div id="liveView" class="videoView">
        <button id="webcamButton" class="mdc-button mdc-button--raised">
        <span class="mdc-button__ripple"></span>
        <span class="mdc-button__label">ENABLE WEBCAM</span>
        </button>
        <div style="position: relative;">
        <video id="webcam" autoplay playsinline></video>
        <canvas class="output_canvas" id="output_canvas" width="1280" height="720" style="position: absolute; left: 0px; top: 0px;"></canvas>
        <p id='gesture_output' class="output">
        </div>
    </div>
    </section>

    <script type="module" src="./static/js/hand_gesture_recognizer.js"></script>
    ''', unsafe_allow_html=True)



st.write(" ")
st.markdown("""<style>.white-bold-text {color: #FAFAFA;font-family: 'Thaoma', monospace;font-size: 25px;font-weight: bold;
        text-decoration: none; display: flex;
        justify-content: center;align-items: center;
        text-align: center;border: 1px solid #262730; 
        border-radius: 6px;  padding: 10px;  
        background-color: #262735;width: 24%;}</style>""",
    unsafe_allow_html=True)

st.markdown('<a href="record_voice" target="_self" class="white-bold-text">Next Step</a>', unsafe_allow_html=True )


