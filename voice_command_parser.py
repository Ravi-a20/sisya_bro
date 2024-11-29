import os
import subprocess
import pyaudio
import json
from vosk import Model, KaldiRecognizer
import time

# Load the VOSK model
model = Model(r"E:\FUN_projects\assistant\vosk_model\vosk-model-small-en-us-0.15")  # Use raw string for path
recognizer = KaldiRecognizer(model, 16000)

# Initialize microphone
mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

print("Listening for commands... (say 'exit' to quit)")

def execute_command(command):
    """Execute system commands based on recognized text."""
    try:
        print(f"Executing command: {command}")  # Debugging output

        # Check for various ways to say "open chrome"
        if "open chrome" in command or "google chrome" in command or "chrome" in command:
            print("Opening Chrome...")
            subprocess.run(["start", "chrome"], shell=True)
        elif "open notepad" in command or "open note pad" in command:
            print("Opening Notepad...")
            subprocess.run(["notepad"], shell=True)
        elif "open calculator" in command or "open calc" in command:
            print("Opening Calculator...")
            subprocess.run(["calc"], shell=True)
        elif "open settings" in command:
            print("Opening Settings...")
            subprocess.run(["start", "ms-settings:"], shell=True)
        elif "shutdown" in command:
            print("Shutting down the system...")
            subprocess.run(["shutdown", "/s", "/t", "1"], shell=True)
        elif "exit" in command:
            print("Exiting...")
            stream.stop_stream()
            stream.close()
            mic.terminate()
            exit(0)
        else:
            print("Command not recognized!")
    except Exception as e:
        print(f"An error occurred: {e}")

def listen_for_command():
    """Listen for a command for 5 seconds and process it."""
    print("Listening for 5 seconds...")  # Confirm the listening starts

    # Start a timer for 5 seconds
    start_time = time.time()
    recognized_command = ""

    while time.time() - start_time < 5:  # Listen for 5 seconds
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            recognized_command = result.get("text", "").lower()
            print(f"Recognized: {recognized_command}")
            break  # Stop listening once a command is recognized

    # If a command was recognized, execute it, otherwise inform the user
    if recognized_command.strip():  # If a command was recognized
        execute_command(recognized_command)
    else:
        print("Incorrect command. No valid command recognized.")

try:
    while True:
        listen_for_command()  # Listen for a command every cycle
except KeyboardInterrupt:
    print("Exiting...")
    stream.stop_stream()
    stream.close()
    mic.terminate()
