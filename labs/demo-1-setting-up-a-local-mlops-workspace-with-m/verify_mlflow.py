# Commands to run in terminal:

# Step 1: Verify Python
# python --version


# Step 2: Create the virtual environment
# python -m venv .venv

# Step 3: Install MLflow
# pip install mlflow


# Step 4: Verify MLflow installation
# mlflow --version


# Step 5: Start the MLflow Tracking Server
# mlflow server --port 5000


# Keep Terminal 1 running.
# Open the MLflow UI in a browser:
# http://127.0.0.1:5000

# Step 6: Run the MLflow verification script
# python verify_mlflow.py


import mlflow
from mlflow.tracking import MlflowClient


TRACKING_URI = "http://127.0.0.1:5000"
EXPERIMENT_NAME = "MLOps Fundamentals"


mlflow.set_tracking_uri(TRACKING_URI)

client = MlflowClient()

experiment = client.get_experiment_by_name(
    EXPERIMENT_NAME
)


if experiment is not None and experiment.lifecycle_stage == "deleted":
    client.restore_experiment(
        experiment.experiment_id
    )

    print("Deleted experiment restored.")
    print()


experiment = mlflow.set_experiment(
    EXPERIMENT_NAME
)


print("MLflow connection successful.")
print()

print("Tracking URI:")
print(mlflow.get_tracking_uri())
print()

print("Experiment Name:")
print(experiment.name)
print()

print("Experiment ID:")
print(experiment.experiment_id)
print()

print("Experiment created or selected successfully.")