import json
import os
import statistics
import time

from dotenv import load_dotenv
import redis


load_dotenv()


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


EXPECTED_RESULTS = int(
    os.getenv(
        "EXPECTED_RESULTS",
        "30"
    )
)


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


print(
    f"Waiting for {EXPECTED_RESULTS} completed jobs..."
)


while (
    redis_client.llen("llm_results")
    < EXPECTED_RESULTS
):

    completed = redis_client.llen(
        "llm_results"
    )

    queued = redis_client.llen(
        "llm_jobs"
    )

    print(
        f"completed={completed:02d} "
        f"queued={queued:02d}",
        end="\r"
    )

    time.sleep(1)


rows = [

    json.loads(item)

    for item in redis_client.lrange(
        "llm_results",
        0,
        -1
    )
]


rows.sort(
    key=lambda item:
    item["finished_at"]
)


successful = [

    item

    for item in rows

    if item["status"] == "ok"
]


if not successful:

    raise SystemExit(
        "No successful jobs."
    )


end_to_end = [

    item["end_to_end_ms"]

    for item in successful
]


processing_times = [

    item["processing_ms"]

    for item in successful
]


start_time = min(
    item["queued_at"]
    for item in successful
)


end_time = max(
    item["finished_at"]
    for item in successful
)


duration = max(
    end_time - start_time,
    0.001
)


throughput = (
    len(successful)
    / duration
)


def percentile(
    values,
    percentile_value
):

    sorted_values = sorted(values)

    index = int(
        round(
            (
                len(sorted_values) - 1
            )
            * percentile_value
        )
    )

    return sorted_values[index]


print(
    "\n\nLoad test results"
)

print(
    "-----------------"
)


print(
    f"Successful jobs : "
    f"{len(successful)}"
)

print(
    f"Duration        : "
    f"{duration:.2f} s"
)

print(
    f"Throughput      : "
    f"{throughput:.2f} jobs/s"
)

print(
    f"Mean E2E latency: "
    f"{statistics.mean(end_to_end):.2f} ms"
)

print(
    f"P50 E2E latency : "
    f"{percentile(end_to_end, 0.50):.2f} ms"
)

print(
    f"P95 E2E latency : "
    f"{percentile(end_to_end, 0.95):.2f} ms"
)

print(
    f"Mean processing : "
    f"{statistics.mean(processing_times):.2f} ms"
)