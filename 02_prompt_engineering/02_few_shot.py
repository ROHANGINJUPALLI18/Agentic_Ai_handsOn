import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# few shot prompting :- directly giving instruction( the prompt) to the LLM and also providing some examples to the LLM in order to get better response from the LLM

SYSTEM_PROMPT = '''

you should only and only ans the coding related questions only and if any non coding question is asked by the user then you should reply with the message "I am designed to answer coding related   questions only" if any thing other than coding question is asked by the user then simply say sorry

q1: expain for loop in python with example ?
a1: for loop in python is used to iterate over a sequence (like list, tuple, string) or other iterable objects. It allows you to execute a block of code repeatedly for each item in the sequence. Here is an example:
for i in range(5):
    print(i)
q2: what is the output of the following code ?
a2: The output of the following code will be:
0
1
2
3
4


'''

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role":"user","content":"code for do while loop in python ?"}
    ]
)

print(response.choices[0].message.content)


