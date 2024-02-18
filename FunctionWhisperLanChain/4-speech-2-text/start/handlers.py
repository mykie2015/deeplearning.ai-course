import requests
import os
import whisper
import ssl


def downloadFile(url, save_path="media/audio.mp3"):
    try:
        # It's recommended to verify SSL certificates
        ssl._create_default_https_context = ssl._create_unverified_context
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"File downloaded successfully and saved to {save_path}")

    except requests.RequestException as e:
        print(f"An error occurred while downloading the file: {e}")


def transcribe(audio_path="media/audio.mp3"):
    try:
        
        # Initialize the Whisper ASR model

        # Your code to transcribe the audio

        # Extract the transcript text from the result

    except Exception as e:
        print(f"An error occurred during transcription: {e}")
