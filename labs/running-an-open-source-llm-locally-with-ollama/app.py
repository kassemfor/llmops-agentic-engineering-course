import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"

print("=" * 60)
print("Local Open-Source LLM with Ollama")
print("=" * 60)

user_prompt = input("\nEnter your prompt: ")

prompt = f"""
You are a helpful AI assistant.
Give clear and concise technical explanations.

User question:
{user_prompt}
"""

payload = {
    "model": MODEL,
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.3
    }
}

print("\nGenerating response locally...\n")

response = requests.post(
    OLLAMA_URL,
    json=payload,
    timeout=120
)

response.raise_for_status()
result = response.json()

print("Model:", MODEL)
print("-" * 60)
print(result["response"])
print("-" * 60)

print("\nLocal inference completed successfully.")