# File: src/transcribe_tests_video.py

import os
import time
import re
import whisper

VIDEO_PATH = "tests/video.mp4"
TRANSCRIPT_PATH = "tests/transcript.txt"

if not os.path.exists(VIDEO_PATH):
    raise FileNotFoundError(f"Input video not found at {VIDEO_PATH}")

print(f"Transcribing {VIDEO_PATH} with Whisper medium.en...")

model = whisper.load_model("turbo")

start = time.time()
result = model.transcribe(VIDEO_PATH)
end = time.time()

# Split transcript into lines for readability
text = result["text"].strip()
# Add newline after ., ?, or ! followed by space
formatted_text = re.sub(r'([.?!])\s+', r'\1\n', text)

os.makedirs(os.path.dirname(TRANSCRIPT_PATH), exist_ok=True)

with open(TRANSCRIPT_PATH, "w", encoding="utf-8") as f:
    f.write(formatted_text)

print(f"Transcript written to {TRANSCRIPT_PATH} in {round(end - start, 2)} s")