import pyaudio
import json
from vosk import Model, KaldiRecognizer

# Load the VOSK model
model = Model(r"E:\FUN_projects\assistant\vosk_model\vosk-model-small-en-us-0.15")  # Replace with the path to your model
recognizer = KaldiRecognizer(model, 16000)

# Initialize microphone
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Listening...")

try:
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            print(f"Recognized: {result.get('text', '')}")
except KeyboardInterrupt:
    print("Exiting...")
    stream.stop_stream()
    stream.close()
    mic.terminate()
