from  huggingface_hub import InferenceClient
import speech_recognition as sr
import pvporcupine
import pyaudio
import struct
import json
import pyttsx3
from dotenv import load_dotenv


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
            Your name is Rick and you are a helpful assistant for musicians to interact with their DAW recording software. 
            You will be given a list of OSC commands that correspond to actions in the DAW that the user would like you to take. 
            The user will then ask you to take actions in the DAW, and you will return the corresponding OSC code so the application can communicate that to the DAW.

            The command document is a list of actions in all caps, followed by their corresponding codes. Here is the list:

            {OSC_pattern}

            For example, if the users tells you "start recording" you would return t/record, because it corresponds to the RECORD action.

            If you are unsure what the user is requesting, say "Sorry, try again." Otherwise, you will reply with only the corresponding code, no more, and then stop. 

            the user's request is:{prompt}
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

    porcupine = pvporcupine.create(
    access_key = "8MiW2e57ER0QQKvCHWpkRhIE9Zhh/0mrurN80SI9LEMfC/7zeUfCrA==",
    keyword_paths = [r"C:\Users\Andrew\OneDrive\Documents\Spinning_Leaf\Rick\hey-rick_en_windows_v3_0_0.ppn"]
    )


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
    OSC_path = r"C:\Users\Andrew\OneDrive\Documents\Spinning_Leaf\Rick\OSC_commands.txt"
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

                print("response: " + generate_response(transcription))

