import streamlit as st
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import tempfile

st.title("YOLO Object Detection App")

# Hard-coded model path
model_path = "trained_model.pt"

# Load the model
try:
    model = YOLO('yolov8n.pt')
    st.sidebar.success("Model loaded successfully!")
except Exception as e:
    st.sidebar.error(f"Error loading model: {e}")

# Sidebar for input selection
st.sidebar.header("Input")
input_type = st.sidebar.radio("Choose input type:", ("Image", "Video"))

if input_type == "Image":
    image_file = st.sidebar.file_uploader("Upload an image:", type=["jpg", "jpeg", "png"])
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # Perform object detection
        results = model(image)
        
        # Display the results
        result_image = results[0].plot(show=False)
        st.image(result_image, caption='Detected Objects', use_column_width=True)

elif input_type == "Video":
    video_file = st.sidebar.file_uploader("Upload a video:", type=["mp4", "avi", "mov"])
    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(video_file.read())
        video = cv2.VideoCapture(tfile.name)
        stframe = st.empty()
        
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = model(frame)
            result_frame = results[0].plot(show=False)
            
            stframe.image(result_frame, channels="RGB", use_column_width=True)
        
        video.release()

st.sidebar.markdown("Developed by [Your Name](https://your-website.com)")
