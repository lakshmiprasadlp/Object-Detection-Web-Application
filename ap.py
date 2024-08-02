import streamlit as st
from PIL import Image
import tempfile
import os

# Set the title of the app
st.title("Image and Video Uploader")

# Create a sidebar for the file uploader
st.sidebar.header("Upload your file")
file = st.sidebar.file_uploader("Upload Image or Video", type=["jpg", "jpeg", "png", "mp4", "avi", "mov"])

if file:
    file_type = file.type.split('/')[0]

    if file_type == 'image':
        st.subheader("Uploaded Image")
        image = Image.open(file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
    elif file_type == 'video':
        st.subheader("Uploaded Video")

        # Save the uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tfile:
            tfile.write(file.read())
            temp_file_path = tfile.name
        
        # Display the video
        st.video(temp_file_path)

        # Cleanup the temporary file after displaying the video
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    else:
        st.warning("Unsupported file type")