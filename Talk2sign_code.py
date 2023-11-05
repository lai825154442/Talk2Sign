import streamlit as st
import openai
from PIL import Image
import requests
from io import BytesIO

openai.api_key = "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"

st.set_page_config(layout="wide", page_title="Voice to Sign Language")

st.write("## Turn voice to sign language")
st.write(
    ":dog: Try uploading an mp3 file to form the sign language. This code is open source and modified by [BackgroundRemoval](https://github.com/tyler-simons/BackgroundRemoval) on GitHub."
)
st.sidebar.write("## Upload mp3 file :gear:")

def upload_mp3(upload):
    audio_file = upload
    return audio_file

def whisper(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file, response_format="text")
    return transcript

def dalle(input_prompt):
    response = openai.Image.create(
        prompt=f"Generate a hand sign image for the text: '{input_prompt}'",
        n=1,
        size="256x256",
    )
    return response

def sl_output(my_upload):
    transcript = upload_mp3(my_upload)
    text = whisper(transcript)
    
    # Split the text into words
    words = text.split()

    # Generate images for each word
    images = []
    for word in words:
        output_image = dalle(word)
        image_url = output_image["data"][0]["url"]
        response = requests.get(image_url)

        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            images.append(image)

    for image, word in zip(images, words):
        st.write(f"Word: {word}")
        st.image(image)

my_upload = st.sidebar.file_uploader("Upload mp3 file", type=["mp3"])

if my_upload is not None:
    sl_output(my_upload)

# Add a button to regenerate results
if st.button("Regenerate Results"):
    sl_output(my_upload)  # This will regenerate the results using the same uploaded file

else:
    st.error("Please upload an mp3 file.")
