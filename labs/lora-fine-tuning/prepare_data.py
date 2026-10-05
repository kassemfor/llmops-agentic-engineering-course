import pandas as pd
from sklearn.model_selection import train_test_split


INPUT_FILE = "data/domain_data.csv"
TRAIN_FILE = "data/train.csv"
EVAL_FILE = "data/eval.csv"


print("Loading domain dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Total records: {len(df)}")


def create_training_text(row):
    return (
        f"### Instruction:\n"
        f"{row['instruction']}\n\n"
        f"### Customer:\n"
        f"{row['input']}\n\n"
        f"### Response:\n"
        f"{row['response']}"
    )


df["text"] = df.apply(
    create_training_text,
    axis=1,
)


train_df, eval_df = train_test_split(
    df[["text"]],
    test_size=0.25,
    random_state=42,
)


train_df.to_csv(
    TRAIN_FILE,
    index=False,
)

eval_df.to_csv(
    EVAL_FILE,
    index=False,
)


print(f"Training records: {len(train_df)}")
print(f"Evaluation records: {len(eval_df)}")

print(f"Training data saved to: {TRAIN_FILE}")
print(f"Evaluation data saved to: {EVAL_FILE}")

print("Dataset preparation completed.")