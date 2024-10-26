
import cv2
import streamlit as st
import mediapipe as mp
import numpy as np



def handGesture():
        
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils

    def recognize_gesture(frame):
        hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)# Draw landmarks on the frame
                height , width , _ = frame.shape
                hand_gesture = classify_gesture(hand_landmarks, height, width)
                cv2.putText(frame, hand_gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA )  
        return frame

    st.title("Hand Gesture Recognition with MediaPipe")
    st.write("This application detects hand gestures and landmarks using MediaPipe.")

    run_webcam = st.checkbox('Run Webcam')
    if run_webcam:
        cap = cv2.VideoCapture(0)
        stframe = st.empty()  # Placeholder for video frames

        while run_webcam:
            cam_on, frame = cap.read()
            if not cam_on:
                st.error("Error: Could not open webcam.")
                break
            
            frame = recognize_gesture(frame)
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            stframe.image(frame_rgb, channels="RGB")       
        cap.release()



def classify_gesture(hand_landmarks, img_width, img_height):
    landmarks = hand_landmarks.landmark

    # Thumb Tip (Landmark 4) and Index Finger Tip (Landmark 8)
    

    WRIST = landmarks[0]
    THUMB_CMC = landmarks[1]
    THUMB_MCP = landmarks[2]
    THUMB_IP = landmarks[3]
    thumb_tip = landmarks[4]
    INDEX_FINGER_MCP = landmarks[5]
    INDEX_FINGER_PIP = landmarks[6]
    INDEX_FINGER_DIP = landmarks[7]
    index_tip = landmarks[8] # INDEX_FINGER_TIP
    MIDDLE_FINGER_MCP = landmarks[9]
    MIDDLE_FINGER_PIP = landmarks[10]
    MIDDLE_FINGER_DIP = landmarks[11]
    MIDDLE_FINGER_TIP = landmarks[12]
    RING_FINGER_MCP = landmarks[13]
    RING_FINGER_PIP = landmarks[14]
    RING_FINGER_DIP = landmarks[15]
    RING_FINGER_TIP = landmarks[16]
    PINKY_MCP = landmarks[17]
    PINKY_PIP = landmarks[18]
    PINKY_DIP = landmarks[19]
    PINKY_TIP = landmarks[20]


    # Convert landmarks to pixel coordinates
    thumb_tip_x, thumb_tip_y = int(thumb_tip.x * img_width), int(thumb_tip.y * img_height)
    index_tip_x, index_tip_y = int(index_tip.x * img_width), int(index_tip.y * img_height)
    middle_tip_x, middle_tip_y = int(middle_tip.x * img_width), int(middle_tip.y * img_height)

    # Logic to classify gestures
    if thumb_tip_y < landmarks[3].y * img_height and index_tip_y > landmarks[6].y * img_height:
        return "Thumb Up"
    elif index_tip_y < landmarks[5].y * img_height and middle_tip_y < landmarks[9].y * img_height:
        return "Victory"
    elif all(landmarks[i].y > landmarks[0].y for i in range(1, 21)):  # All fingers open
        return "Open Hand"
    else:
        return "Unknown Gesture"




'''
0 - Unrecognized gesture, label: Unknown
1 - Closed fist, label: Closed_Fist
2 - Open palm, label: Open_Palm
3 - Pointing up, label: Pointing_Up
4 - Thumbs down, label: Thumb_Down
5 - Thumbs up, label: Thumb_Up
6 - Victory, label: Victory
7 - Love, label: ILoveYou


'''





