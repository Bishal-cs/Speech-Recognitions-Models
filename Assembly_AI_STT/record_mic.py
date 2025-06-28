import pyaudio
import wave
import os
from dotenv import load_dotenv

load_dotenv()
Audio_File_Path = os.getenv("Audio_File")

FRAME_PER_BUFFER = 3200
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000

p = pyaudio.PyAudio()

stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=FRAME_PER_BUFFER
)

print("* recording")

seconds = 5
frames = []

for i in range(0, int(RATE / FRAME_PER_BUFFER * seconds)):
    data = stream.read(FRAME_PER_BUFFER)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()

print("* done")

obj = wave.open(Audio_File_Path, "wb")
obj.setnchannels(CHANNELS)
obj.setsampwidth(p.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b"".join(frames))
obj.close()