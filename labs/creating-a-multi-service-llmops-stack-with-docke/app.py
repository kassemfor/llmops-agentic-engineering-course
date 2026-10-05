import os
import requests

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://ollama:11434/api/generate"
)

MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b"
)

print("=" * 60)
print("Multi-Service LLMOps Stack")
print("=" * 60)

prompt = input("\nEnter your prompt: ")

payload = {
    "model": MODEL,
    "prompt": prompt,
    "stream": False
}

print("\nSending request to Ollama service...\n")

try:
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    result = response.json()

    print("Model:", MODEL)
    print("-" * 60)
    print(result["response"])
    print("-" * 60)

    print("\nInference completed successfully.")

except requests.exceptions.ConnectionError:
    print("Could not connect to the Ollama service.")

except requests.exceptions.RequestException as error:
    print("Request failed:", error)