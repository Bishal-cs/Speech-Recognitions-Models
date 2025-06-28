import requests
import sys 
from api_communication import *

filename = sys.argv[1] if len(sys.argv) > 1 else "Data/Assembly_AI_output.wav"
if not filename.endswith('.wav'):
    print("Please provide a valid .wav file.")
    sys.exit(1)

audio_url = upload_file(filename)
save_transcription(audio_url, filename)