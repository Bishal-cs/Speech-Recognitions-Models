import pyaudio
import asyncio
import websockets
import base64
import json 
from dotenv import load_dotenv
import os
from websockets import exceptions

load_dotenv()
API_KEY = os.getenv("Assembly_AI_API")

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

URL = "wss://api.assemblyai.com/v2/realtime/ws?sample_rate=16000"

async def send_receive():
    async with websockets.connect(
        URL,
        ping_interval=5,
        ping_timeout=20,
        extra_headers = {"Authorization": API_KEY}
    ) as _ws:
        await asyncio.sleep(1)
        session_begin = await _ws.recv()
        print(session_begin)
        print("Sending audio...")

        async def send():
            while True:
                try:
                    data = stream.read(FRAME_PER_BUFFER, exception_on_overflow=False)
                    data = base64.b64encode(data).decode("utf-8")
                    json_data = json.dumps({"audio": data})
                    await _ws.send(json_data)
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                asyncio.sleep(0.01)

        async def receive():
            while True:
                try:
                    result_str = await _ws.recv()
                    result = json.loads(result_str)
                    prompt = result["text"]
                    if prompt and result["message_type"] == "FinalTranscript":
                        print(f"User: {prompt}")
                except websockets.exceptions.ConnectionClosedError as e:
                    print(e)
                    assert e.code == 4008
                    break
                except Exception as e:
                    assert False, "Not a websocket 4008 error"
                asyncio.sleep(0.01)
                
        send_result, receive_result = await asyncio.gather(send(), receive())

asyncio.run(send_receive())

async def main():
    pass