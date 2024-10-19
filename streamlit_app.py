import streamlit as st
import websocket
import json
import pyaudio
import threading

# AssemblyAI API key
API_KEY = '788835bce5f4408b864bd438b695379a'

# Streamlit App
st.title("Real-Time Speech to Text Transcription")
st.write("Speak something...")

# Placeholder for displaying transcription
transcription_placeholder = st.empty()

# Audio stream settings
CHUNK = 4096  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # 16-bit PCM format
CHANNELS = 1  # Mono audio
RATE = 16000  # Sample rate in Hz (required by AssemblyAI)

# Initialize PyAudio
audio = pyaudio.PyAudio()

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

    # Open the microphone stream and send audio data in chunks
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    def send_audio():
        try:
            while True:
                data = stream.read(CHUNK, exception_on_overflow=False)
                ws.send(data, opcode=websocket.ABNF.OPCODE_BINARY)
        except Exception as e:
            print(f"Error sending audio: {e}")

    # Run the audio stream in a separate thread
    threading.Thread(target=send_audio).start()

# Start the WebSocket connection to AssemblyAI
def start_transcription():
    ws_url = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={RATE}"
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
    start_transcription()
