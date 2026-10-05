import argparse
import json
import os
import time

from dotenv import load_dotenv
import redis


load_dotenv()


parser = argparse.ArgumentParser()

parser.add_argument(
    "--jobs",
    type=int,
    default=30
)

parser.add_argument(
    "--delay",
    type=float,
    default=0.05
)

args = parser.parse_args()


REDIS_HOST = os.getenv(
    "REDIS_HOST",
    "localhost"
)

REDIS_PORT = int(
    os.getenv(
        "REDIS_PORT",
        "6379"
    )
)


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


prompts = [

    "Explain continuous integration for LLM applications in two sentences.",

    "What is a canary deployment?",

    "Why is queue depth useful for autoscaling?",

    "Explain prompt regression in simple terms.",

    "Why do LLM systems need quality gates?"

]


redis_client.delete(
    "llm_results"
)


for index in range(args.jobs):

    job = {

        "job_id":
            f"job-{index + 1:03d}",

        "prompt":
            prompts[
                index % len(prompts)
            ],

        "queued_at":
            time.time()
    }


    redis_client.rpush(
        "llm_jobs",
        json.dumps(job)
    )


    print(
        f'Queued {job["job_id"]}'
    )


    time.sleep(
        args.delay
    )


print(
    f"\nQueued {args.jobs} jobs."
)

print(
    "Watch Kubernetes replicas scale while workers drain the queue."
)