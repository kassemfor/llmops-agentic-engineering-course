import os
import pandas as pd

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY was not found in the .env file.")


class TrainingExample(BaseModel):
    text: str
    label: str


client = genai.Client(api_key=API_KEY)

seed_df = pd.read_csv("data/seed_data.csv")

print("Seed dataset:")
print(seed_df)

seed_examples = seed_df[["text", "label"]].to_dict(orient="records")

prompt = f"""
We are creating synthetic training data for a customer-support
text classification model.

The allowed labels are:

- billing
- technical
- account

Here are existing labelled examples:

{seed_examples}

Generate exactly 12 NEW customer-support examples.

Requirements:
1. Generate 4 examples for each label.
2. Keep each example realistic and concise.
3. Do not copy the existing examples.
4. Use only the allowed labels.
5. Do not include names, email addresses, phone numbers,
   account numbers, or other personal information.
"""

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=prompt,
    config=types.GenerateContentConfig(
        temperature=0.8,
        response_mime_type="application/json",
        response_schema=list[TrainingExample],
    ),
)

generated_examples = response.parsed

synthetic_df = pd.DataFrame(
    [example.model_dump() for example in generated_examples]
)

synthetic_df.insert(
    0,
    "id",
    range(
        len(seed_df) + 1,
        len(seed_df) + len(synthetic_df) + 1,
    ),
)

synthetic_df.to_csv(
    "data/synthetic_data.csv",
    index=False,
)

print("\nGenerated synthetic examples:")
print(synthetic_df)

print(
    f"\nSaved {len(synthetic_df)} synthetic records "
    "to data/synthetic_data.csv"
)

client.close()