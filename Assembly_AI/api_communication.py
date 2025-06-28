import requests
import time
from dotenv import load_dotenv
import os

# Load API Key using dotenv....
load_dotenv()
API_KEY = os.getenv("Assembly_AI_API")

# upload in the server
upload_endpoint = 'https://api.assemblyai.com/v2/upload'
transcript_endpoint = 'https://api.assemblyai.com/v2/transcript'

headers = {'authorization': API_KEY}

def upload_file(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data 

    upload_response = requests.post(
        upload_endpoint,
        headers=headers,
        data = read_file(filename)
    )
    audio_url = upload_response.json()['upload_url']   
    return audio_url

"""This is transcribe the file on the server."""

# audio url from the response
def transcribtion(audio_url):
    transcript_request = {"audio_url": audio_url}
    transcript_response = requests.post(
        transcript_endpoint,
        json=transcript_request,
        headers=headers
    )
    job_id = transcript_response.json()['id']
    return job_id

# Polling the server
def polling_transcript(transcript_id):
    polling_endpoint = f'{transcript_endpoint}/{transcript_id}'
    pooling_response = requests.get(polling_endpoint, headers=headers)
    return pooling_response.json()

# Get the response from the server
def get_transcription_result_url(audio_url):
    transcript_id = transcribtion(audio_url)
    while True:
        data = polling_transcript(transcript_id)
        if data['status'] == 'completed':
            return data, None
        elif data['status'] == 'error':
            return data, data['error']
    
        print("Processing in progress...")
        time.sleep(30)

# save the result from the server
def save_transcription(audio_url, filename):
    data, error = get_transcription_result_url(audio_url)

    if error:
        print("Something went wrong !!!.", error)
    elif data:
        text_filename = filename + '.txt'
        with open(text_filename, 'w') as f:
            f.write(data['text'])
        print(f"Transcript saved to {text_filename}")
    else:
        print("Something went wrong !!!.")