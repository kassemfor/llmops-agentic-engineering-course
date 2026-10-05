import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel


load_dotenv()

app = FastAPI(
    title="Gemini Canary Deployment Demo"
)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-3.5-flash-lite"
)

PROMPT_VERSION = os.getenv(
    "PROMPT_VERSION",
    "v1"
)

RELEASE_NAME = os.getenv(
    "RELEASE_NAME",
    "stable"
)


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_PROMPTS = {

    "v1": """
You are a concise DevOps tutor.

Explain technical concepts in simple language.

Keep answers short and practical.

Use no more than three short sentences.
""",

    "v2": """
You are a concise LLMOps tutor.

Explain technical concepts in simple language.

Keep answers short and practical.

When relevant, also mention production safety,
reliability, or controlled deployment practices.

Use no more than three short sentences.
"""

}


class AskRequest(BaseModel):
    question: str


@app.get("/")
def root():

    return {
        "message": "Gemini Canary Deployment Demo",
        "release": RELEASE_NAME,
        "prompt_version": PROMPT_VERSION,
        "model": MODEL_NAME
    }


@app.get("/health")
def health():

    return {
        "status": "healthy",
        "release": RELEASE_NAME,
        "prompt_version": PROMPT_VERSION,
        "model": MODEL_NAME
    }


@app.post("/ask")
def ask(request: AskRequest):

    started = time.perf_counter()

    system_prompt = SYSTEM_PROMPTS.get(
        PROMPT_VERSION,
        SYSTEM_PROMPTS["v1"]
    )

    try:

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=request.question,

            config=types.GenerateContentConfig(

                system_instruction=system_prompt,

                temperature=0.2,

                max_output_tokens=180

            )

        )

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc


    latency_ms = round(
        (
            time.perf_counter()
            - started
        ) * 1000,
        2
    )


    return {

        "release": RELEASE_NAME,

        "prompt_version": PROMPT_VERSION,

        "model": MODEL_NAME,

        "latency_ms": latency_ms,

        "answer": response.text

    }