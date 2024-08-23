from  huggingface_hub import InferenceClient
import speech_recognition as sr
import pvporcupine
import pyaudio
import struct
import json
import pyttsx3
import os
import sys
from dotenv import load_dotenv
from pathlib import Path


"""
0) Download model
1) Open Mic for passive listening
Get OSC state from reaper
2) Recognize wake word
3) record further
4) process audio to text
5) send text to llm
5) Receive OSC Code from LLM
- Send OSC code to Reaper via TCP
6) Speak back response
Return to passive listening
"""


def speak_text(text):
    """
    This function speaks the input text out loud using the pyttsx3 library.
    """

    speech_to_text_engine.say(text)
    speech_to_text_engine.runAndWait()



def generate_response(prompt):

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



if __name__ == "__main__":

    print("Initializing")

    load_dotenv()

    # Init text-to-speech engine

    speech_to_text_engine = pyttsx3.init()

    # Init hotword detector

    rick_audio_file = "hey-rick_en_windows_v3_0_0.ppn"

    working_directory = Path.cwd()

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

    # Load OSC pattern

    OSC_txt_file = "OSC_commands.txt"
    OSC_path = working_directory / OSC_txt_file

    with open(OSC_path, "r") as file:
        OSC_pattern = file.read()

    
    print("ready")

    while True:

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
                    print("Whisper could not understand the audio")
                except Exception as ex:
                    print("Error during recognition:", ex)

                print("transcription: " + transcription)

                response = generate_response(transcription)

                print(response)

                OSC_code = response.strip().split()[-1]

                if OSC_code == "EXIT":
                    sys.exit()

                print(OSC_code)



