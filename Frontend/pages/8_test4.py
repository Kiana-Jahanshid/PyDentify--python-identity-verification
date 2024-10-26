import streamlit as st
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np
import time
from mediapipe.framework.formats import landmark_pb2

# Local Modules
import content
import utils
# import plotting


st.error("!! This Demo is currently not working !!", icon="🚨")


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult

# Set up MediaPipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Global variables
COUNTER, FPS = 0, 0
START_TIME = time.time()
recognition_result = None


def save_result(result: GestureRecognizerResult ,unused_output_image: mp.Image,timestamp_ms: int): # type: ignore
    global recognition_result
    recognition_result = result


@st.cache_resource
def load_model(model_path, num_hands=2):
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=VisionRunningMode.LIVE_STREAM,
        num_hands=num_hands,
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        result_callback=save_result,
    )
    return vision.GestureRecognizer.create_from_options(options)


def process_frame(frame, recognizer):
    global COUNTER, FPS, START_TIME, recognition_result

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    recognizer.recognize_async(mp_image, time.time_ns() // 1_000_000)

    COUNTER += 1
    if COUNTER % 10 == 0:
        FPS = 10 / (time.time() - START_TIME)
        START_TIME = time.time()

    if recognition_result:
        frame = draw_landmarks_and_gestures(frame, recognition_result)

    cv2.putText(
        frame,
        f"FPS = {FPS:.1f}",
        (24, 50),
        cv2.FONT_HERSHEY_DUPLEX,
        1,
        (0, 0, 0),
        1,
        cv2.LINE_AA,
    )
    return frame


def draw_landmarks_and_gestures(frame, result):
    if result.hand_landmarks:
        for hand_index, hand_landmarks in enumerate(result.hand_landmarks):
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            hand_landmarks_proto.landmark.extend(
                [
                    landmark_pb2.NormalizedLandmark(
                        x=landmark.x, y=landmark.y, z=landmark.z
                    )
                    for landmark in hand_landmarks
                ]
            )
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks_proto,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )

            if result.gestures:
                gesture = result.gestures[hand_index]
                category_name = gesture[0].category_name
                score = round(gesture[0].score, 2)
                result_text = f"{category_name} ({score})"

                frame_height, frame_width = frame.shape[:2]
                x_min = min([landmark.x for landmark in hand_landmarks])
                y_min = min([landmark.y for landmark in hand_landmarks])
                x_min_px = int(x_min * frame_width)
                y_min_px = int(y_min * frame_height)

                cv2.putText(
                    frame,
                    result_text,
                    (x_min_px, y_min_px - 10),
                    cv2.FONT_HERSHEY_DUPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
    return frame


st.title("Hand Gesture Recognition")

# Sidebar
model_path, num_hands = utils.mediapipe_sidebar_options()

# Load the model
recognizer = load_model(model_path, num_hands)

# Content
content.content_mediapipe_hgr_task_webcam()

# Create columns
col1, col2 = st.columns(2)

# Placeholder for video feed
with col1:
    st.markdown("## 🎥 Video Feed:")
    video_placeholder = st.empty()
    col11, col12 = st.columns([1, 1])
    with col11:
        run_button = st.button(
            ":green[Run]", type="secondary", use_container_width=True
        )
    with col12:
        stop_button = st.button("Stop", type="primary", use_container_width=True)

# Placeholder for gesture recognition results
with col2:
    st.markdown("## 🗂️ Model Prediction:")
    st.markdown("### Hand Gestures:")
    gesture_text = st.empty()

if run_button:
    with st.spinner("Open webcam..."):
        cap = cv2.VideoCapture(0)  # Use 0 for default webcam
    if not cap.isOpened():
        st.error("Could not open webcam.")

    while True:
        success, frame = cap.read()
        if not success:
            st.warning("Failed to read frame from webcam.", icon="⚠️")
            break

        frame = cv2.flip(frame, 1)
        processed_frame = process_frame(frame, recognizer)
        video_placeholder.image(processed_frame, channels="BGR", use_column_width=True)

        if recognition_result and recognition_result.gestures:
            gesture_info = []
            for hand_index, gestures in enumerate(recognition_result.gestures):
                for gesture in gestures:
                    gesture_info.append(
                        f"✋ Hand {hand_index + 1}: Model predicts the Class/Gesture **:red[{gesture.category_name}]** "
                        f"with a Probability/Score of **:red[{gesture.score:.2f}]**"
                    )
            all_gestures = "\n\n".join(gesture_info)
            gesture_text.markdown(all_gestures)

        # Check for stop button
        if stop_button:
            break

    # Release resources
    cap.release()
    recognizer.close()