import requests
import sys 
from Assembly_AI.api_communication import *

filename = sys.argv[1]


audio_url = upload_file(filename)
save_transcription(audio_url, filename)