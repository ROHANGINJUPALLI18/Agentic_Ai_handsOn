from openai import OpenAI
from dotenv import load_dotenv
import os
import requests

load_dotenv()

def get_weeather(city:str):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather in {city.lower()} is {response.text}"
    
    return f"Some thing went wrong"

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def main():
    user_query = input(">")
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role":"user","content":user_query}
        ]
    )
    
    print(f"🤖:{response.choices[0].message.content}")
    
print(get_weeather("delhi"))
