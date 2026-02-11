import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# zero shot prompting :- directly giving instruction( the prompt) to the LLM
SYSTEM_PROMPT='you should only and only ans the coding related questions only and if any non coding question is asked by the user then you should reply with the message "I am designed to answer coding related questions only" if any thing other than coding question is asked by the user then simply say sorry'

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role":"user","content":"what is the value of a+b whole square ?"}
    ]
)

print(response.choices[0].message.content)


