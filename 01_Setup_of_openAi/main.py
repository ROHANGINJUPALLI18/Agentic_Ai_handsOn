from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"user","content":"hey hi how are you and what is your name and who are you ?"}
    ]
)

print(response.choices[0].message.content)


'''
we are using the gemini api by the openAi google library

'''