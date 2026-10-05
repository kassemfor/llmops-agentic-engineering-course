import mlflow
import mlflow.sklearn

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score


mlflow.set_tracking_uri(
    "http://127.0.0.1:5000"
)

mlflow.set_experiment(
    "MLOps Fundamentals"
)


data = load_diabetes()

X = data.data
y = data.target


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


alpha = 1.0


with mlflow.start_run():

    model = Ridge(
        alpha=alpha
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(
        X_test
    )

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    mlflow.log_param(
        "alpha",
        alpha
    )

    mlflow.log_metric(
        "rmse",
        rmse
    )

    mlflow.log_metric(
        "r2",
        r2
    )

    mlflow.sklearn.log_model(
        model,
        name="ridge_model"
    )

    print(
        "Experiment completed successfully."
    )

    print(f"Alpha: {alpha}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.2f}")