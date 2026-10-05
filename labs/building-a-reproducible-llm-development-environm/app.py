import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Add it to the .env file."
    )

client = genai.Client(api_key=api_key)

print("=" * 60)
print("Reproducible LLM Application")
print("=" * 60)

prompt = input("\nEnter your prompt: ")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

print("\nLLM Response:")
print("-" * 60)
print(response.text)
print("-" * 60)

print("\nApplication executed successfully.")