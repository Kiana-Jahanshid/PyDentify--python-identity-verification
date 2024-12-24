import streamlit as st
# from st_audiorec import st_audiorec
#from audiorecorder import audiorecorder
from streamlit_audio_recorder.st_audiorec.__init__ import st_audiorec

st.title("Please record your voice :")

user_voice = st_audiorec()
#user_voice= audiorecorder("Click to record", "Stop recording")

if user_voice is not None:
    #audio = st.audio(user_voice, format='audio/wav')
    with open("./output/user_voice.wav", "wb") as f:
        f.write(user_voice)

    ##  audiorecorder 
    # st.audio(user_voice.export().read()) 
    # user_voice.export("./output/user_voice_2.wav" , format="wav")
    # st.write(f"Frame rate: {user_voice.frame_rate}, Frame width: {user_voice.frame_width}, Duration: {user_voice.duration_seconds} seconds")

st.write(" ")
st.write(" ")
st.markdown("""<style>.white-bold-text {color: #FAFAFA;font-family: 'Thaoma', monospace;font-size: 25px;font-weight: bold;
        text-decoration: none; display: flex;
        justify-content: center;align-items: center;
        text-align: center;border: 1px solid #262730; 
        border-radius: 6px;  padding: 10px;  
        background-color: #262735;width: 24%;}</style>""",
    unsafe_allow_html=True)

st.markdown('<a href="hand_gesture" target="_self" class="white-bold-text">Next Step</a>', unsafe_allow_html=True )

#st.page_link("pages/2_take_picture.py", label='Next Stage ⏭', use_container_width=True  )
#st.link_button("Next Stage ⏭", "take_picture")

