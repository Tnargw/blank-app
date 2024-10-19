import streamlit as st
import requests
import assemblyai as aai
import time  # Import time for sleep
from streamlit_mic_recorder import speech_to_text

state = st.session_state


# Set up AssemblyAI API key
aai.settings.api_key = "788835bce5f4408b864bd438b695379a"

# Title for the app
st.title("Trascribe and Translate!")
tab1, tab2, tab3 = st.tabs(["Record Audio", "Input MP3/MP4", "Secret"])

state.text_received = []


with tab1:    
        st.write("Convert speech to text:")
        text = speech_to_text(language='en', use_container_width=True, just_once=True, key='STT')
        state.text_received.append(text)
        for text in state.text_received:
            st.text(text)



# File uploader for MP3 and MP4 files
with tab2:
    uploaded_file = st.file_uploader("Choose an MP3 or MP4 file", type=["mp3", "mp4"])

if uploaded_file is not None:
    # Read the file as bytes
    audio_bytes = uploaded_file.read()
    
    # Upload audio to AssemblyAI
    headers = {
        'authorization': aai.settings.api_key,
        'content-type': 'application/json'
    }
    upload_url = "https://api.assemblyai.com/v2/upload"
    
    # Send the audio file to AssemblyAI
    response = requests.post(upload_url, headers=headers, data=audio_bytes)
    
    if response.status_code == 200:
        upload_response = response.json()
        audio_url = upload_response['upload_url']
        
        # Transcribe the audio file
        transcript_response = aai.Transcriber().transcribe(audio_url)
        
        # Wait for the transcription to complete
        while transcript_response.status != 'completed':
            time.sleep(5)  # Wait for a few seconds before checking again
            transcript_response = aai.Transcriber().get_by_id(transcript_response.id)
        
        # Retrieve the transcription text
        transcript_text = transcript_response.text
        st.write("Transcription:")
        st.write(transcript_text)
    else:
        st.error("Error uploading audio file: " + response.text)

with tab3:
     if st.button("DO NOT PUSH"):
        st.balloons()



# Ima go back to the land of dis where it runs on my own computer... Nevermind it doesnt run on dis