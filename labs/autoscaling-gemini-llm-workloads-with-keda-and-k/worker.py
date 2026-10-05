import json
import os
import socket
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
import redis


load_dotenv()


REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

QUEUE_NAME = os.getenv("QUEUE_NAME", "llm_jobs")
RESULTS_NAME = os.getenv("RESULTS_NAME", "llm_results")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-3.5-flash-lite"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=None
)


worker_name = socket.gethostname()


print(
    f"Worker started: {worker_name}",
    flush=True
)


while True:

    item = redis_client.blpop(
        QUEUE_NAME,
        timeout=0
    )


    if not item:
        continue


    _, raw_job = item

    job = json.loads(raw_job)


    started_at = time.time()


    try:

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=job["prompt"],

            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=120
            )
        )


        status = "ok"

        answer = response.text

        error = None


    except Exception as exc:

        status = "error"

        answer = None

        error = str(exc)


    finished_at = time.time()


    result = {

        "job_id": job["job_id"],

        "worker": worker_name,

        "status": status,

        "queued_at": job["queued_at"],

        "started_at": started_at,

        "finished_at": finished_at,

        "queue_wait_ms": round(
            (
                started_at
                - job["queued_at"]
            ) * 1000,
            2
        ),

        "processing_ms": round(
            (
                finished_at
                - started_at
            ) * 1000,
            2
        ),

        "end_to_end_ms": round(
            (
                finished_at
                - job["queued_at"]
            ) * 1000,
            2
        ),

        "answer": answer,

        "error": error
    }


    redis_client.rpush(
        RESULTS_NAME,
        json.dumps(result)
    )


    print(
        f'Completed {job["job_id"]} | '
        f'worker={worker_name} | '
        f'wait={result["queue_wait_ms"]} ms | '
        f'process={result["processing_ms"]} ms',
        flush=True
    )