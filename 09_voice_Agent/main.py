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
    # the below line will convert the AI response text to speech
    speech = gTTS(text=text, lang="en")
    # the below lines will save the generated speech to a file and play it back to the user, you can use any other TTS API and audio player as well
    filename = "response.mp3"
    # the below line will save the generated speech to a file named response.mp3, you can change the filename as per your requirement
    speech.save(filename)
    # the below line will play the generated speech file using the playsound library, you can use any other audio player library as well
    playsound(filename)


def main():
    r = sr.Recognizer() # Speech to Text
    # the below line will access the microphone of the system to listen to the user audio, you can use any other audio input method as well
    with sr.Microphone() as source: # Mic Access
        # adjust the recognize sensitivity to ambient noise and record audio from the microphone
        r.adjust_for_ambient_noise(source)
        # you can adjust the pause threshold according to your need. It is the number of seconds of non-speaking audio before a phrase is considered complete
        r.pause_threshold = 2
        # this is the system prompt 
        SYSTEM_PROMPT = f"""
                You're an expert voice agent. You are given the transcript of what
                user has said using voice.
                You need to output as if you are an voice agent and whatever you speak
                will be converted back to audio using AI and played back to user.
            """
            
        # to keep the chat memory for the conversation 
        messages = [
            { "role": "system", "content": SYSTEM_PROMPT },
        ]
        
        # for the unlimited chat between user and AI agent we will use while loop
        while True:

            print("Speak Something...")
            # listen to the audio from the user 
            audio = r.listen(source)
            print("Processing Audio... (STT)")
            # the below line will convert the user audio to text using Google's speech recognition API, you can use any other STT API as well
            stt = r.recognize_google(audio)

            print("You Said:", stt)
            # append the user message to the messages list which will be sent to the Gemini API to generate response from the AI agent
            messages.append({ "role": "user", "content": stt })
            # the below lines will call the Gemini API to generate response from the AI agent based on the user message and system prompt, you can use any other LLM API as well
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=messages
            )
            # append the AI response to the messages list which will be used as context for the next user message, this will help in maintaining the conversation history and context for the AI agent
            messages.append({ "role": "assistant", "content": response.choices[0].message.content })
            print("AI Response", response.choices[0].message.content)
            # the below line will convert the AI response to speech and play it back to the user
            tts(text=response.choices[0].message.content)
            
main()