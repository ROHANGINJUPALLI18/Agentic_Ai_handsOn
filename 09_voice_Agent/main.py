from dotenv import load_dotenv
import os
from gtts import gTTS
from playsound3 import playsound
import speech_recognition as sr
from openai import  OpenAI
from openai.helpers import LocalAudioPlayer

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


# Text to Speech
def tts(text):
    speech = gTTS(text=text, lang="en")
    filename = "response.mp3"
    speech.save(filename)
    playsound(filename)


def main():
    r = sr.Recognizer() # Speech to Text
    
    with sr.Microphone() as source: # Mic Access
        # adjust the recognize sensitivity to ambient noise and record audio from the microphone
        r.adjust_for_ambient_noise(source)
        # you can adjust the pause threshold according to your need. It is the number of seconds of non-speaking audio before a phrase is considered complete
        r.pause_threshold = 2
        
        SYSTEM_PROMPT = f"""
                You're an expert voice agent. You are given the transcript of what
                user has said using voice.
                You need to output as if you are an voice agent and whatever you speak
                will be converted back to audio using AI and played back to user.
            """
        messages = [
            { "role": "system", "content": SYSTEM_PROMPT },
        ]
        
        while True:

            print("Speak Something...")
            audio = r.listen(source)

            print("Processing Audio... (STT)")
            stt = r.recognize_google(audio)

            print("You Said:", stt)

            messages.append({ "role": "user", "content": stt })

            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=messages
            )
            messages.append({ "role": "assistant", "content": response.choices[0].message.content })
            print("AI Response", response.choices[0].message.content)
            # the below line will convert the AI response to speech and play it back to the user
            tts(text=response.choices[0].message.content)
            
main()