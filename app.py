
import streamlit as st
import openai
import os
from deepgram import Deepgram
import requests
import json
from io import BytesIO

# Initialize OpenAI API key
openai.api_key = "sk-proj-Mp4A1ybtGLTn9I64554eT3BlbkFJW8r52Dyr7LjaGDHVbSHn"

# Initialize Deepgram API key
DEEPGRAM_API_KEY = "39e1ce9cddd0d876499ca722b473064f25fdc76e"
deepgram = Deepgram(DEEPGRAM_API_KEY)

# Function to convert speech to text using Deepgram API
def transcribe_audio(file):
    source = {'buffer': file, 'mimetype': 'audio/wav'}
    response = deepgram.transcription.prerecorded(source, {'punctuate': True})
    return response['results']['channels'][0]['alternatives'][0]['transcript']

# Function to convert text to speech using an external TTS API
def generate_speech(text):
    url = "https://api.deepgram.com/v1/tts"
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice": "en-US-Wavenet-D"  # You can customize the voice
    }
    response = requests.post(url, headers=headers, json=data)
    return response.content

# Streamlit app
def main():
    st.title("Speech-to-Text and Text-to-Speech App")

    # Upload audio file
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
    if audio_file:
        # Transcribe audio to text
        audio_bytes = audio_file.read()
        transcript = transcribe_audio(audio_bytes)
        st.write("Transcription:")
        st.write(transcript)

        # Get response from OpenAI GPT-3.5
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=transcript,
            max_tokens=150
        )
        response_text = response['choices'][0]['text'].strip()
        st.write("GPT-3.5 Response:")
        st.write(response_text)

        # Generate speech from response text
        response_audio = generate_speech(response_text)

        # Play the generated audio
        st.audio(BytesIO(response_audio), format='audio/mp3')

if _name_ == '_main_':
    main()