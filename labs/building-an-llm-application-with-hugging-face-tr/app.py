from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "google/flan-t5-small"

print("=" * 60)
print("Hugging Face Transformers - Local LLM Inference")
print("=" * 60)

print("\nLoading tokenizer and model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME
)

print("Model loaded successfully.")

prompt = input("\nEnter your prompt: ")

print("\nTokenizing prompt...")

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

print("Generating response...\n")

outputs = model.generate(
    **inputs,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.7
)

response = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)

print("Model:", MODEL_NAME)
print("-" * 60)
print(response)
print("-" * 60)

print("\nInference completed successfully.")