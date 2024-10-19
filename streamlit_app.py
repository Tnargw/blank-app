import streamlit as st
import sounddevice as sd
import numpy as np
import json
import websocket
import threading

# AssemblyAI API key
API_KEY = '788835bce5f4408b864bd438b695379a'

# Streamlit App
st.title("Real-Time Speech to Text Transcription")
st.write("Speak something...")

# Placeholder for displaying transcription
transcription_placeholder = st.empty()

# Audio stream settings
SAMPLE_RATE = 16000
CHUNK_SIZE = 4096

# Function to handle incoming WebSocket messages
def on_message(ws, message):
    response = json.loads(message)
    if 'text' in response:
        transcription_placeholder.markdown(f"**Transcription:** {response['text']}")

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket Closed: {close_status_code}, {close_msg}")

def on_open(ws):
    print("WebSocket Connection Opened")

    # Callback to process and send audio
    def callback(indata, frames, time, status):
        if status:
            print(status)
        ws.send(indata.tobytes(), opcode=websocket.ABNF.OPCODE_BINARY)

    # Start the sounddevice stream and send audio in chunks
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=callback, blocksize=CHUNK_SIZE):
        st.write("Streaming audio...")

# Start the WebSocket connection to AssemblyAI
def start_transcription():
    ws_url = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}"
    ws = websocket.WebSocketApp(
        ws_url,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open,
        header={"Authorization": API_KEY}
    )
    ws.run_forever()

# Streamlit button to start transcription
if st.button("Start Transcription"):
    threading.Thread(target=start_transcription).start()
