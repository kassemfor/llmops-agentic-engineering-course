import json
import time
from collections import Counter

import requests


URL = "http://localhost:8080/ask"

TOTAL_REQUESTS = 20


results = Counter()


for request_number in range(
    1,
    TOTAL_REQUESTS + 1
):

    try:

        response = requests.post(

            URL,

            json={
                "question":
                "Why is a canary deployment useful for LLM applications?"
            },

            timeout=60

        )

        response.raise_for_status()

        data = response.json()


        release_key = (
            f'{data["release"]}:'
            f'{data["prompt_version"]}'
        )


        results[release_key] += 1


        answer_preview = (
            data["answer"]
            .replace("\n", " ")
            [:90]
        )


        print(
            f"{request_number:02d} | "
            f"{release_key:12s} | "
            f"{data['latency_ms']:8.2f} ms | "
            f"{answer_preview}"
        )


    except Exception as exc:

        print(
            f"{request_number:02d} | "
            f"ERROR | {exc}"
        )


    time.sleep(0.3)


print("\nTraffic distribution")

print(
    json.dumps(
        results,
        indent=2
    )
)