import pandas as pd


SEED_FILE = "data/seed_data.csv"
SYNTHETIC_FILE = "data/synthetic_data.csv"
OUTPUT_FILE = "data/final_training_data.csv"

ALLOWED_LABELS = {
    "billing",
    "technical",
    "account",
}

seed_df = pd.read_csv(SEED_FILE)
synthetic_df = pd.read_csv(SYNTHETIC_FILE)

print("SYNTHETIC DATA VALIDATION")

print(f"\nSynthetic records received: {len(synthetic_df)}")

required_columns = {"text", "label"}

missing_columns = required_columns - set(synthetic_df.columns)

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

print("Required columns: PASS")

before = len(synthetic_df)

synthetic_df = synthetic_df.dropna(
    subset=["text", "label"]
)

removed_missing = before - len(synthetic_df)

print(
    f"Missing-value records removed: {removed_missing}"
)

synthetic_df["text"] = (
    synthetic_df["text"]
    .astype(str)
    .str.strip()
)

synthetic_df["label"] = (
    synthetic_df["label"]
    .astype(str)
    .str.strip()
    .str.lower()
)

synthetic_df = synthetic_df[
    synthetic_df["text"].str.len() > 0
]

invalid_mask = ~synthetic_df["label"].isin(
    ALLOWED_LABELS
)

invalid_count = invalid_mask.sum()

if invalid_count:
    print(
        f"Invalid-label records removed: {invalid_count}"
    )

synthetic_df = synthetic_df[
    ~invalid_mask
].copy()

before = len(synthetic_df)

synthetic_df["_normalized_text"] = (
    synthetic_df["text"]
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

synthetic_df = synthetic_df.drop_duplicates(
    subset=["_normalized_text"]
)

removed_duplicates = before - len(synthetic_df)

print(
    f"Duplicate synthetic records removed: "
    f"{removed_duplicates}"
)

seed_normalized = (
    seed_df["text"]
    .astype(str)
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

before = len(synthetic_df)

synthetic_df = synthetic_df[
    ~synthetic_df["_normalized_text"].isin(
        seed_normalized
    )
]

seed_duplicates = before - len(synthetic_df)

print(
    f"Records duplicating seed data removed: "
    f"{seed_duplicates}"
)

synthetic_df = synthetic_df.drop(
    columns=["_normalized_text"]
)

seed_df["source"] = "original"
synthetic_df["source"] = "synthetic"

final_df = pd.concat(
    [seed_df, synthetic_df],
    ignore_index=True,
)

final_df["id"] = range(
    1,
    len(final_df) + 1,
)

print("LABEL DISTRIBUTION")

distribution = final_df["label"].value_counts()

percentages = (
    final_df["label"]
    .value_counts(normalize=True)
    .mul(100)
    .round(1)
)

for label in sorted(ALLOWED_LABELS):
    count = distribution.get(label, 0)
    percentage = percentages.get(label, 0)

    print(
        f"{label:<12}: "
        f"{count:>2} records "
        f"({percentage:>5.1f}%)"
    )

print("\n" + "=" * 55)
print("BASIC DATASET BIAS CHECK")
print("=" * 55)

largest_share = percentages.max()
smallest_share = percentages.min()

if largest_share > 50:
    print(
        "WARNING: One label represents more than "
        "50% of the dataset."
    )
else:
    print(
        "Label dominance check: PASS"
    )

if smallest_share < 20:
    print(
        "WARNING: At least one label represents "
        "less than 20% of the dataset."
    )
else:
    print(
        "Minimum representation check: PASS"
    )

final_df["word_count"] = (
    final_df["text"]
    .str.split()
    .str.len()
)

length_by_label = (
    final_df
    .groupby("label")["word_count"]
    .mean()
    .round(1)
)

print("\nAverage text length by label:")

print(length_by_label)

if (
    length_by_label.max()
    > length_by_label.min() * 2
):
    print(
        "\nWARNING: Large differences in text "
        "length exist between labels."
    )
else:
    print(
        "\nText-length consistency check: PASS"
    )

final_df = final_df.drop(
    columns=["word_count"]
)

final_df.to_csv(
    OUTPUT_FILE,
    index=False,
)

print("VALIDATION COMPLETE")

print(
    f"Final dataset size: {len(final_df)} records"
)

print(
    f"Clean dataset saved to: {OUTPUT_FILE}"
)