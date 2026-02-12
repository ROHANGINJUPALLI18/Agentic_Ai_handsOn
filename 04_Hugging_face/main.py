from transformers import pipeline

pipe = pipeline("text-generation", model="google/gemma-3-270m-it")
messages = [
    {"role": "user", "content": "Who are you?"},
]

# Generate response with explicit parameters to avoid conflicts
response = pipe(
    messages,
    max_new_tokens=20,  # Limit new tokens instead of total length
    pad_token_id=pipe.tokenizer.eos_token_id  # Prevent warning about pad token
)
print(response)