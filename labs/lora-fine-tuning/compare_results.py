import pandas as pd


RESULTS_FILE = "output/results.csv"


print("=" * 60)
print("HYPERPARAMETER COMPARISON")
print("=" * 60)


results = pd.read_csv(
    RESULTS_FILE
)


print("\nTraining results:\n")

print(
    results.to_string(
        index=False
    )
)


best_index = (
    results["evaluation_loss"]
    .idxmin()
)

best = results.loc[
    best_index
]


print("\n" + "=" * 60)
print("BEST CONFIGURATION")
print("=" * 60)

print(
    f"Configuration: "
    f"{best['configuration']}"
)

print(
    f"LoRA rank: "
    f"{int(best['lora_rank'])}"
)

print(
    f"LoRA alpha: "
    f"{int(best['lora_alpha'])}"
)

print(
    f"Learning rate: "
    f"{best['learning_rate']}"
)

print(
    f"Epochs: "
    f"{int(best['epochs'])}"
)

print(
    f"Training loss: "
    f"{best['training_loss']:.4f}"
)

print(
    f"Evaluation loss: "
    f"{best['evaluation_loss']:.4f}"
)

print(
    "\nLower evaluation loss indicates "
    "the better result for this experiment."
)