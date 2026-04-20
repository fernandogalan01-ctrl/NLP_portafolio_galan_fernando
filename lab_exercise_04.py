import os
import platform
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
from textblob import TextBlob
# Local Text to Speech (TTS) using pyttsx3
def local_tts(text, filename="local_tts_output.mp3"):
    print("Executing Local TTS")
    engine = pyttsx3.init()
    engine.setProperty('rate', 105)  # Set speech rate
    engine.say(text)
    engine.save_to_file(text, filename)
    engine.runAndWait()
# External Text to Speech (TTS) using gTTS (Google Text-to-Speech API)
def external_tts(text, filename="external_tts_output.mp3"):
    print("Executing External API TTS Google Text-to-Speech")
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)
    system = platform.system() 
    os.system(f"start {filename}")
# Load Local Audio File using SpeechRecognition
def load_audio_file(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        print(f"Loading Local Audio File: {file_path}...]")
        # Record the audio data from the file
        audio_data = recognizer.record(source) 
        print("Audio File Loaded Successfully")
        return recognizer, audio_data
# Execution Flow
if __name__ == "__main__":
    print("SPEECH TASKS PIPELINE")
    # Test Local TTS
    local_tts("Hello. This is my local text to speech running offline.")
    # Test External TTS
    external_tts("And this is the external API text to speech running online.")
    load_audio_file("C:\\Users\\ferga\\Documents\\Nueva carpeta\\NLP_portafolio_galan_fernando-1\\local_stt_input.wav")
    
    
