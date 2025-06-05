import speech_recognition as sr
import pvporcupine
import pyaudio
import pyttsx3
import os
import sys
import socket
import struct
import json
import asyncio
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from dotenv import load_dotenv
from pathlib import Path
from pythonosc import udp_client
from huggingface_hub import InferenceClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "tauri://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_local_ip():
    """
    Gets local_ip for communication to DAW
    """

    # Creates socket using IPv4 and UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.settimeout(0)
    
    try:
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    
    return IP

def speak_text(text):
    """
    This function speaks the input text out loud using the pyttsx3 library.
    """

    speech_to_text_engine.say(text)

    #TODO Do we really need this extra
    speech_to_text_engine.runAndWait()



def generate_response(prompt):

    """
    Calls the LLM API for a response. 
    """

    repo_id = "microsoft/Phi-3-mini-4k-instruct"

    inference_client = InferenceClient(model = repo_id)

    prompt = f"""
            <|system|>

            Your name is Rick and you are a helpful assistant for musicians to interact with their Digital Audio Workstation software. 
            
            For example, it could be DAW software like Reaper, ProTools, or Logic. 
            
            You will be given a list of OSC commands that correspond to actions in the DAW that the user would like you to take. 
            
            This list is written in pairs, with a single all caps word first being the desired actions name, and then it's code. A string with a single letter, followed by a slash, followed by that all caps word in lower case. 
            
            For example, if the user wanted to pause, they might say "pause playback". In that case, the correspoinding code would be the "t/pause" in "PAUSE t/pause".
            
            The application will take that code and use it to communicate with the DAW to take the user's requested action. 

            Here is the list: "{OSC_pattern}"

            The user will only give you a single request, do not return more than one response. You will return the code, and only the single code, and then stop. 
            
            If you are unsure what the user is requesting, say "Sorry, try again." 
            
            Also, the user may ask you to turn off. If they say something like "stop" or "turn off" or "goodbye", then return just the string "EXIT"<|end|>

            <|user|>
            
            "{prompt}" <|end|>

            <|assistant|>
"""
    
    response = inference_client.post(
        json={
            "inputs": prompt,
            "parameters": {"max_new_tokens": 200},
            "task": "text-generation",
        },
    )

    return json.loads(response.decode())[0]["generated_text"]

@app.get("/")
async def read_root():
    logger.info("Root endpoint called")
    return {"message": "Rick is running!"}

@app.get("/api/status")
async def get_status():
    logger.info("Status endpoint called")
    return {"status": "active"}

def run_voice_recognition():
    """
    Function to run the voice recognition loop
    """
    global porcupine, audio_stream, speech_to_text_engine

    print("Voice recognition started")

    while True:
        try:
            # Reading audio data from the stream
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
            
            # Processing audio data using Porcupine
            keyword_index = porcupine.process(keyword)
            
            # Checking if a hotword is detected
            if keyword_index >= 0:
                speak_text("Yo")

                # Begin Recording
                filename = "input.wav"

                with sr.Microphone() as source: 
                    recognizer = sr.Recognizer()
                
                    audio1 = recognizer.listen(source)
                    
                    try:
                        transcription = recognizer.recognize_whisper(audio1)
                    except sr.UnknownValueError:
                        logger.error("Whisper could not understand the audio")
                        continue
                    except Exception as ex:
                        logger.error(f"Error during recognition: {ex}")
                        continue

                    logger.info(f"transcription: {transcription}")

                    response = generate_response(transcription)

                    logger.info(f"Response: {response}")

                    OSC_code = response.strip().split()[-1]

                    if OSC_code == "EXIT":
                        sys.exit()

                    logger.info(f"OSC code: {OSC_code}")

                    # Send to DAW via OSC/UDP
                    local_ip = get_local_ip()
                    reaper_port = 55444
                    client = udp_client.SimpleUDPClient("192.168.4.207", reaper_port)
                    client.send_message("action/1007", 1)

        except Exception as e:
            logger.error(f"Error in voice recognition loop: {e}")
            continue

if __name__ == "__main__":
    print("Initializing")

    load_dotenv()

    working_directory = Path.cwd()

    # Load OSC pattern
    OSC_txt_file = "OSC_commands.txt"
    OSC_path = working_directory / OSC_txt_file

    with open(OSC_path, "r") as file:
        OSC_pattern = file.read()

    # Init hotword detector
    rick_audio_file = "hey-rick_en_windows_v3_0_0.ppn"
    rick_path = working_directory / rick_audio_file

    porcupine = pvporcupine.create(
        access_key = os.getenv("PORCUPINE_TOKEN"),
        keyword_paths = [str(rick_path)])

    # Init audio stream
    paud = pyaudio.PyAudio()

    audio_stream = paud.open(
        rate = porcupine.sample_rate,
        channels= 1,
        format= pyaudio.paInt16,
        input = True,
        frames_per_buffer= porcupine.frame_length
    )
    
    # Init text-to-speech engine
    speech_to_text_engine = pyttsx3.init()
    
    print("ready")

    # Start voice recognition in a separate thread
    voice_thread = threading.Thread(target=run_voice_recognition, daemon=True)
    voice_thread.start()

    try:
        # Get port from command line arguments or use default
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
        logger.info(f"Starting server on port {port}")
        
        # Run the FastAPI server
        uvicorn.run(app, host="127.0.0.1", port=port, log_level="info")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)







                







