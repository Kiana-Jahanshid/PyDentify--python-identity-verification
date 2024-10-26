import cv2
import av
import streamlit as st
import numpy as np
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
TF_ENABLE_ONEDNN_OPTS=0

model_path = os.path.abspath("gesture_recognizer.task")
print(model_path)
# STEP 2: Create an GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
VisionRunningMode = mp.tasks.vision.RunningMode
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils


class HandTrackingTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img = cv2.flip(img, 1)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #results = hands.process(img_rgb)
        recognition_result = recognizer.recognize(img_rgb)

        top_gesture = recognition_result.gestures[0][0]
        hand_landmarks = recognition_result.hand_landmarks

        if recognition_result.multi_hand_landmarks: # Draw hand landmarks on the image if any hands are detected
            for hand_landmarks in recognition_result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        return img , hand_landmarks , top_gesture

webrtc_streamer(key="hand-tracking", video_transformer_factory=HandTrackingTransformer)












