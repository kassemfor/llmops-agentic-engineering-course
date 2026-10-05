import pandas as pd
import mlflow


DATA_FILE = "data/llm_requests.csv"
RESULT_FILE = "monitoring_results.csv"

TRACKING_URI = "http://127.0.0.1:5000"
EXPERIMENT_NAME = "LLM Monitoring"


print("Starting LLM monitoring workflow...")


# Connect to MLflow
mlflow.set_tracking_uri(TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)


# Load monitoring data
df = pd.read_csv(DATA_FILE)

print(f"Total requests: {len(df)}")


# Calculate response length
df["response_length"] = df["response"].str.len()


# Calculate monitoring metrics
avg_latency = df["latency_ms"].mean()
avg_quality = df["quality_score"].mean()
avg_safety = df["safety_score"].mean()
avg_response_length = df["response_length"].mean()


# Identify requests that need attention
slow_requests = (df["latency_ms"] > 800).sum()
low_quality_requests = (df["quality_score"] < 0.80).sum()


# Log monitoring metrics to MLflow
with mlflow.start_run(run_name="LLM_Monitoring_Run"):

    mlflow.log_metric(
        "average_latency_ms",
        avg_latency
    )

    mlflow.log_metric(
        "average_quality_score",
        avg_quality
    )

    mlflow.log_metric(
        "average_safety_score",
        avg_safety
    )

    mlflow.log_metric(
        "average_response_length",
        avg_response_length
    )

    mlflow.log_metric(
        "total_requests",
        len(df)
    )

    mlflow.log_metric(
        "slow_requests",
        slow_requests
    )

    mlflow.log_metric(
        "low_quality_requests",
        low_quality_requests
    )


# Save monitoring results
df.to_csv(
    RESULT_FILE,
    index=False
)


print()
print("Monitoring Summary")
print("------------------")

print(f"Average Latency: {avg_latency:.2f} ms")
print(f"Average Quality Score: {avg_quality:.2f}")
print(f"Average Safety Score: {avg_safety:.2f}")
print(f"Average Response Length: {avg_response_length:.2f}")

print()
print(f"Slow Requests: {slow_requests}")
print(f"Low Quality Requests: {low_quality_requests}")

print()
print(f"Results saved to: {RESULT_FILE}")
print("Monitoring completed successfully.")