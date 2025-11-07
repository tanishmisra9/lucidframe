import whisper
import os
import time

# Input file
file_path = "tests/audio.m4a"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"Audio file not found: {file_path}")

# Models to test
models = {
    "tiny.en": "tiny.en",
    "base.en": "base.en",
    "small.en": "small.en",
    "medium.en": "medium.en",
    "large": "large",
    "turbo": "turbo"
}

results = "tests/model_comparison.txt"

with open(results, "w", encoding="utf-8") as f:
    f.write("LUCIDFRAME MODEL COMPARISON\n")
    f.write("============================\n\n")

    for name, model_name in models.items():
        print(f"\n--- Running {model_name} ---")
        start_time = time.time()

        model = whisper.load_model(model_name)
        result = model.transcribe(file_path)

        end_time = time.time()
        elapsed = round(end_time - start_time, 2)

        # Save to file
        f.write(f"MODEL: {name}\n")
        f.write(f"Execution Time: {elapsed} seconds\n")
        f.write("Transcription:\n")
        f.write(result["text"].strip() + "\n")
        f.write("-" * 40 + "\n\n")

        # Print progress
        print(f"{model_name} done in {elapsed}s")

print(f"\nResults saved to {results}")
