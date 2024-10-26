import streamlit as st
from streamlit.components.v1 import html
TF_ENABLE_ONEDNN_OPTS=0
import streamlit.components.v1 as components

st.title("Match your hand's gesture with patterns:")

#enable = st.checkbox("Enable camera")
#hand_img = st.camera_input("Bring your hand in front of camera" , disabled= not enable )


# Define HTML and JavaScript for MediaPipe Hand Tracking
mediapipe_code = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>MediaPipe Hand Tracking</title>
    <style>
        video {
            width: 100%;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <h3>Webcam Stream for Hand Gesture Recognition</h3>
    <video id="videoElement" autoplay></video>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"></script>
    <script>
        const videoElement = document.getElementById('videoElement');

        const hands = new Hands({
            locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`,
        });
        hands.setOptions({
            maxNumHands: 2,
            modelComplexity: 1,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5,
        });
        hands.onResults(onResults);

        const camera = new Camera(videoElement, {
            onFrame: async () => {
                await hands.send({ image: videoElement });
            },
            width: 1280,
            height: 720,
        });
        camera.start();

        function onResults(results) {
            console.log(results);
            // Use this to visualize the detected hands or perform other custom actions.
        }
    </script>
</body>
</html>
"""


components.html('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        video {
            width: 100%;
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <link rel="stylesheet" href="./static/css/mediapipe_handGesture.css">
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

    <script>
        import {
        GestureRecognizer,
        FilesetResolver,
        DrawingUtils
        } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3";

        const demosSection = document.getElementById("demos");
        let gestureRecognizer: GestureRecognizer;
        let runningMode = "IMAGE";
        let enableWebcamButton: HTMLButtonElement;
        let webcamRunning: Boolean = false;
        const videoHeight = "360px";
        const videoWidth = "480px";

        // Before we can use HandLandmarker class we must wait for it to finish
        // loading. Machine Learning models can be large and take a moment to
        // get everything needed to run.
        const createGestureRecognizer = async () => {
        const vision = await FilesetResolver.forVisionTasks(
            "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.3/wasm"
        );
        gestureRecognizer = await GestureRecognizer.createFromOptions(vision, {
            baseOptions: {
            modelAssetPath:
                "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
            delegate: "GPU"
            },
            runningMode: runningMode
        });
        demosSection.classList.remove("invisible");
        };
        createGestureRecognizer();

        /********************************************************************
        // Demo 1: Detect hand gestures in images
        ********************************************************************/

        const imageContainers = document.getElementsByClassName("detectOnClick");

        for (let i = 0; i < imageContainers.length; i++) {
        imageContainers[i].children[0].addEventListener("click", handleClick);
        }

        async function handleClick(event) {
        if (!gestureRecognizer) {
            alert("Please wait for gestureRecognizer to load");
            return;
        }

        if (runningMode === "VIDEO") {
            runningMode = "IMAGE";
            await gestureRecognizer.setOptions({ runningMode: "IMAGE" });
        }
        // Remove all previous landmarks
        const allCanvas = event.target.parentNode.getElementsByClassName("canvas");
        for (var i = allCanvas.length - 1; i >= 0; i--) {
            const n = allCanvas[i];
            n.parentNode.removeChild(n);
        }

        const results = gestureRecognizer.recognize(event.target);

        // View results in the console to see their format
        console.log(results);
        if (results.gestures.length > 0) {
            const p = event.target.parentNode.childNodes[3];
            p.setAttribute("class", "info");

            const categoryName = results.gestures[0][0].categoryName;
            const categoryScore = parseFloat(
            results.gestures[0][0].score * 100
            ).toFixed(2);
            const handedness = results.handednesses[0][0].displayName;

            p.innerText = `GestureRecognizer: ${categoryName}\n Confidence: ${categoryScore}%\n Handedness: ${handedness}`;
            p.style =
            "left: 0px;" +
            "top: " +
            event.target.height +
            "px; " +
            "width: " +
            (event.target.width - 10) +
            "px;";

            const canvas = document.createElement("canvas");
            canvas.setAttribute("class", "canvas");
            canvas.setAttribute("width", event.target.naturalWidth + "px");
            canvas.setAttribute("height", event.target.naturalHeight + "px");
            canvas.style =
            "left: 0px;" +
            "top: 0px;" +
            "width: " +
            event.target.width +
            "px;" +
            "height: " +
            event.target.height +
            "px;";

            event.target.parentNode.appendChild(canvas);
            const canvasCtx = canvas.getContext("2d");
            const drawingUtils = new DrawingUtils(canvasCtx);
            for (const landmarks of results.landmarks) {
            drawingUtils.drawConnectors(
                landmarks,
                GestureRecognizer.HAND_CONNECTIONS,
                {
                color: "#00FF00",
                lineWidth: 5
                }
            );
            drawingUtils.drawLandmarks(landmarks, {
                color: "#FF0000",
                lineWidth: 1
            });
            }
        }
        }

        /********************************************************************
        // Demo 2: Continuously grab image from webcam stream and detect it.
        ********************************************************************/

        const video = document.getElementById("webcam");
        const canvasElement = document.getElementById("output_canvas");
        const canvasCtx = canvasElement.getContext("2d");
        const gestureOutput = document.getElementById("gesture_output");

        // Check if webcam access is supported.
        function hasGetUserMedia() {
        return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
        }

        // If webcam supported, add event listener to button for when user
        // wants to activate it.
        if (hasGetUserMedia()) {
        enableWebcamButton = document.getElementById("webcamButton");
        enableWebcamButton.addEventListener("click", enableCam);
        } else {
        console.warn("getUserMedia() is not supported by your browser");
        }

        // Enable the live webcam view and start detection.
        function enableCam(event) {
        if (!gestureRecognizer) {
            alert("Please wait for gestureRecognizer to load");
            return;
        }

        if (webcamRunning === true) {
            webcamRunning = false;
            enableWebcamButton.innerText = "ENABLE PREDICTIONS";
        } else {
            webcamRunning = true;
            enableWebcamButton.innerText = "DISABLE PREDICTIONS";
        }

        // getUsermedia parameters.
        const constraints = {
            video: true
        };

        // Activate the webcam stream.
        navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
            video.srcObject = stream;
            video.addEventListener("loadeddata", predictWebcam);
        });
        }

        let lastVideoTime = -1;
        let results = undefined;
        async function predictWebcam() {
        const webcamElement = document.getElementById("webcam");
        // Now let's start detecting the stream.
        if (runningMode === "IMAGE") {
            runningMode = "VIDEO";
            await gestureRecognizer.setOptions({ runningMode: "VIDEO" });
        }
        let nowInMs = Date.now();
        if (video.currentTime !== lastVideoTime) {
            lastVideoTime = video.currentTime;
            results = gestureRecognizer.recognizeForVideo(video, nowInMs);
        }

        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
        const drawingUtils = new DrawingUtils(canvasCtx);

        canvasElement.style.height = videoHeight;
        webcamElement.style.height = videoHeight;
        canvasElement.style.width = videoWidth;
        webcamElement.style.width = videoWidth;

        if (results.landmarks) {
            for (const landmarks of results.landmarks) {
            drawingUtils.drawConnectors(
                landmarks,
                GestureRecognizer.HAND_CONNECTIONS,
                {
                color: "#00FF00",
                lineWidth: 5
                }
            );
            drawingUtils.drawLandmarks(landmarks, {
                color: "#FF0000",
                lineWidth: 2
            });
            }
        }
        canvasCtx.restore();
        if (results.gestures.length > 0) {
            gestureOutput.style.display = "block";
            gestureOutput.style.width = videoWidth;
            const categoryName = results.gestures[0][0].categoryName;
            const categoryScore = parseFloat(
            results.gestures[0][0].score * 100
            ).toFixed(2);
            const handedness = results.handednesses[0][0].displayName;
            gestureOutput.innerText = `GestureRecognizer: ${categoryName}\n Confidence: ${categoryScore} %\n Handedness: ${handedness}`;
        } else {
            gestureOutput.style.display = "none";
        }
        // Call this function again to keep predicting when the browser is ready.
        if (webcamRunning === true) {
            window.requestAnimationFrame(predictWebcam);
        }
        }    
    </script>
                
</body>
</html>
    ''',  height=600)



st.write(" ")
st.markdown("""<style>.white-bold-text {color: #FAFAFA;font-family: 'Thaoma', monospace;font-size: 25px;font-weight: bold;
        text-decoration: none; display: flex;
        justify-content: center;align-items: center;
        text-align: center;border: 1px solid #262730; 
        border-radius: 6px;  padding: 10px;  
        background-color: #262735;width: 24%;}</style>""",
    unsafe_allow_html=True)

st.markdown('<a href="record_voice" target="_self" class="white-bold-text">Next Step</a>', unsafe_allow_html=True )


