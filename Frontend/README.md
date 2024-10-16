
# how to run 

```
streamlit run app.py
```

# how to connect streamlit into MongoDB :

https://docs.streamlit.io/develop/tutorials/databases/mongodb


# recording voice part :

+ here we can use 2 library for recording voice in streamlit :

## [1_ streamlit-audiorec:](https://github.com/stefanrmmr/streamlit-audio-recorder)
Here , i DIDN'T INSTALL this package with pip (pip install streamlit-audiorec), i have colned streamlit-audiorec repository and modified it (removed delete button from ui). <br>
And i have import its main function like this : ``` from streamlit_audio_recorder.st_audiorec.__init__ import st_audiorec ``` in ```3_record_voice.py``` .


## [2_ streamlit-audiorecorder :](https://github.com/theevann/streamlit-audiorecorder)
how to install :
```
pip install streamlit-audiorecorder
```