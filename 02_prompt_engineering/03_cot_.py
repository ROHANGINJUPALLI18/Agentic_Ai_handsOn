import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """
You answer only coding-related questions.
If the question is not about coding, reply exactly:
I am designed to answer coding related questions only

Always respond in JSON with this schema:
{"step": "start|plan|output", "content": "string"}

Rules:
- Use step=start to acknowledge the task briefly.
- Use step=plan to provide a short, high-level plan (no hidden reasoning).
- Use step=output for the final answer.
"""

print("\n\n")

message_history = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_query = input(">> ").strip()
    if not user_query:
        continue

    message_history.append({"role": "user", "content": user_query})

    while True:
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            response_format={"type": "json_object"},
            messages=message_history
        )

        raw_result = response.choices[0].message.content
        parse_result = json.loads(raw_result)

        message_history.append({"role": "assistant", "content": raw_result})

        step = str(parse_result.get("step", "")).lower()
        content = str(parse_result.get("content", ""))

        if step == "start":
            print("[START]", content)
            continue

        if step == "plan":
            print("[PLAN]", content)
            continue

        if step == "output":
            print("[OUTPUT]", content)
            print("\n\n")
            break

        print("[INFO]", content)
        print("\n\n")
        break


