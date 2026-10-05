import os
import csv
import torch

from datasets import load_dataset

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

from peft import (
    LoraConfig,
    TaskType,
    get_peft_model,
)


MODEL_NAME = "HuggingFaceTB/SmolLM2-135M-Instruct"

TRAIN_FILE = "data/train.csv"
EVAL_FILE = "data/eval.csv"

RESULTS_FILE = "output/results.csv"


os.makedirs(
    "output",
    exist_ok=True,
)


print("Loading dataset...")

dataset = load_dataset(
    "csv",
    data_files={
        "train": TRAIN_FILE,
        "validation": EVAL_FILE,
    },
)


print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


def tokenize_function(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=256,
    )


print("Tokenizing dataset...")

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["text"],
)


data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)


CONFIGURATIONS = [
    {
        "name": "config_1",
        "r": 4,
        "alpha": 8,
        "learning_rate": 2e-4,
        "epochs": 2,
    },
    {
        "name": "config_2",
        "r": 8,
        "alpha": 16,
        "learning_rate": 1e-4,
        "epochs": 3,
    },
]


results = []


for config in CONFIGURATIONS:

    print("\n" + "=" * 60)
    print(
        f"TRAINING {config['name'].upper()}"
    )
    print("=" * 60)

    print(
        f"LoRA rank: {config['r']}"
    )

    print(
        f"LoRA alpha: {config['alpha']}"
    )

    print(
        f"Learning rate: "
        f"{config['learning_rate']}"
    )

    print(
        f"Epochs: {config['epochs']}"
    )


    print("\nLoading base model...")

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
    )


    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=config["r"],
        lora_alpha=config["alpha"],
        lora_dropout=0.05,
        target_modules=[
            "q_proj",
            "v_proj",
        ],
        bias="none",
    )


    print("Applying LoRA adapter...")

    model = get_peft_model(
        model,
        lora_config,
    )


    print("\nTrainable parameters:")

    model.print_trainable_parameters()


    output_dir = (
        f"output/{config['name']}"
    )


    training_args = TrainingArguments(
        output_dir=output_dir,

        learning_rate=(
            config["learning_rate"]
        ),

        num_train_epochs=(
            config["epochs"]
        ),

        per_device_train_batch_size=2,
        per_device_eval_batch_size=2,

        gradient_accumulation_steps=2,

        eval_strategy="epoch",
        save_strategy="no",

        logging_steps=1,

        report_to="none",

        fp16=torch.cuda.is_available(),

        use_cpu=not torch.cuda.is_available(),
    )


    trainer = Trainer(
        model=model,
        args=training_args,

        train_dataset=(
            tokenized_dataset["train"]
        ),

        eval_dataset=(
            tokenized_dataset["validation"]
        ),

        data_collator=data_collator,
    )


    print("\nStarting fine-tuning...")

    train_result = trainer.train()


    print("\nEvaluating model...")

    eval_result = trainer.evaluate()


    train_loss = (
        train_result.training_loss
    )

    eval_loss = (
        eval_result["eval_loss"]
    )


    print(
        f"\nTraining loss: "
        f"{train_loss:.4f}"
    )

    print(
        f"Evaluation loss: "
        f"{eval_loss:.4f}"
    )


    print("\nSaving LoRA adapter...")

    model.save_pretrained(
        output_dir
    )

    tokenizer.save_pretrained(
        output_dir
    )


    results.append(
        {
            "configuration": (
                config["name"]
            ),
            "lora_rank": (
                config["r"]
            ),
            "lora_alpha": (
                config["alpha"]
            ),
            "learning_rate": (
                config["learning_rate"]
            ),
            "epochs": (
                config["epochs"]
            ),
            "training_loss": (
                train_loss
            ),
            "evaluation_loss": (
                eval_loss
            ),
        }
    )


    del model
    del trainer

    if torch.cuda.is_available():
        torch.cuda.empty_cache()


with open(
    RESULTS_FILE,
    "w",
    newline="",
) as file:

    writer = csv.DictWriter(
        file,
        fieldnames=results[0].keys(),
    )

    writer.writeheader()
    writer.writerows(results)


print("\n" + "=" * 60)
print("TRAINING COMPLETE")
print("=" * 60)

print(
    f"Results saved to: {RESULTS_FILE}"
)