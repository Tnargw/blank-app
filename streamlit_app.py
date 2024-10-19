import streamlit as st
import json
import pyaudio
import asyncio
import websockets

# AssemblyAI API key
API_KEY = '788835bce5f4408b864bd438b695379a'

# Streamlit App
st.title("Real-Time Speech to Text Transcription")
st.write("Speak something Pl0x...")

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
async def on_message(websocket):
    async for message in websocket:
        response = json.loads(message)
        if 'text' in response:
            transcription_placeholder.markdown(f"**Transcription:** {response['text']}")

async def on_open(websocket):
    print("WebSocket Connection Opened")

    # Open the microphone stream and send audio data in chunks
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    # Sending audio data to WebSocket in chunks
    while True:
        try:
            data = stream.read(CHUNK, exception_on_overflow=False)
            await websocket.send(data)
        except Exception as e:
            print(f"Error sending audio: {e}")
            break

# WebSocket connection to AssemblyAI using websockets
async def start_transcription():
    ws_url = f"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={RATE}"
    headers = {
        "Authorization": API_KEY
    }
    
    # Connect to AssemblyAI WebSocket
    async with websockets.connect(ws_url, extra_headers=headers) as websocket:
        await on_open(websocket)
        await on_message(websocket)

# Streamlit button to start transcription
if st.button("Start Transcription"):
    st.write("Transcription started...")
    
    # Run the WebSocket connection and microphone streaming in a single async event loop
    asyncio.run(start_transcription())
