import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

class HandGestureRecognizer(VideoTransformerBase):
    def __init__(self):
        # Initialize MediaPipe hands model
        self.hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def classify_gesture(self, hand_landmarks):
        # Here, you can add gesture classification logic based on landmarks
        # For demonstration, we return a dummy gesture based on the number of landmarks
        if hand_landmarks:
            return "Open Hand"  # Example gesture
        return "Unknown Gesture"
    
    def transform(self, frame):
        # Convert frame to RGB as MediaPipe uses RGB images
        image = frame.to_ndarray(format="bgr24")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process image to detect hands
        results = self.hands.process(image_rgb)
        print("ressssssssssss" , results)
        gesture_text = "No Hands Detected"
        
        if results.multi_hand_landmarks:
            # Draw hand landmarks on the image
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2)
                )

                # Classify gesture based on hand landmarks
                gesture_text = self.classify_gesture(hand_landmarks)

        # Get image height and width to position the text
        height, width, _ = image.shape
        
        # Set the text's position (bottom center of the video)
        text_position = (int(width * 0.3), height - 10)
        
        # Put the recognized gesture name on the video frame
        cv2.putText(image, f'Gesture: {gesture_text}', text_position, cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Return the frame with the hand landmarks and gesture name drawn on it
        return image

# Start the WebRTC streamer for video capture and gesture recognition
webrtc_ctx = webrtc_streamer(
    key="hand-gesture-recognition",
    mode=WebRtcMode.SENDRECV,
    video_transformer_factory=HandGestureRecognizer,
    media_stream_constraints={"video": True, "audio": False},
    async_transform=True
)



