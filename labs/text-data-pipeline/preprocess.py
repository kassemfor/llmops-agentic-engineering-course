import pandas as pd


INPUT_FILE = "data/raw_data.csv"
OUTPUT_FILE = "data/processed_data.csv"


print("Starting text preprocessing pipeline...")


# Load the raw dataset
df = pd.read_csv(INPUT_FILE)

print(f"Raw records: {len(df)}")


# Remove rows with missing text
df = df.dropna(subset=["text"])


# Remove extra whitespace
df["text"] = df["text"].str.strip()


# Remove empty text records
df = df[df["text"] != ""]


# Remove duplicate text records
df = df.drop_duplicates(
    subset=["text"]
)


# Reset row indexes
df = df.reset_index(drop=True)


# Save the processed dataset
df.to_csv(
    OUTPUT_FILE,
    index=False
)


print(f"Processed records: {len(df)}")
print(f"Removed records: {10 - len(df)}")
print(f"Processed dataset saved to: {OUTPUT_FILE}")
print("Preprocessing completed successfully.")