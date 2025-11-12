import tkinter as tk
from tkinter import messagebox
import cv2
import threading
import subprocess
import time
import os
import whisper

VIDEO_PATH = "tests/video.mp4"
TRANSCRIPT_PATH = "tests/transcript.txt"
DEVICE = "0:1"  # camera 0, microphone 1 for MacBook Pro

recording = False
ffmpeg_proc = None

# ----------------- Webcam Preview -----------------
def show_frame():
    ret, frame = cap.read()
    if ret:
        img = cv2.resize(frame, (640, 360))
        cv2.imshow("LucidFrame Demo", img)
    if recording:
        window.after(10, show_frame)
    else:
        cv2.destroyAllWindows()

# ----------------- Recording Functions -----------------
def start_recording():
    global recording, ffmpeg_proc

    os.makedirs("tests", exist_ok=True)

    cmd = [
        "ffmpeg",
        "-f", "avfoundation",
        "-framerate", "30",
        "-video_size", "1280x720",
        "-i", DEVICE,
        "-thread_queue_size", "512",
        "-use_wallclock_as_timestamps", "1",
        "-vsync", "1",
        "-async", "1",
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-c:a", "aac",
        "-shortest",
        "-y",
        VIDEO_PATH,
    ]

    try:
        ffmpeg_proc = subprocess.Popen(cmd)
        recording = True
        record_btn.config(state="disabled")
        stop_btn.config(state="normal")
        show_frame()
        print("Recording started...")
    except Exception as e:
        messagebox.showerror("Error", f"Could not start recording:\n{e}")

def stop_recording():
    global recording, ffmpeg_proc
    recording = False
    if ffmpeg_proc:
        ffmpeg_proc.terminate()
        ffmpeg_proc.wait()
        ffmpeg_proc = None
    record_btn.config(state="normal")
    stop_btn.config(state="disabled")
    print("Recording stopped.")
    transcribe_thread = threading.Thread(target=transcribe_video)
    transcribe_thread.start()

# ----------------- Transcription -----------------
def transcribe_video():
    try:
        if not os.path.exists(VIDEO_PATH):
            messagebox.showerror("Error", "No recorded video found.")
            return

        print(f"Transcribing {VIDEO_PATH} with Whisper medium.en...")
        model = whisper.load_model("medium.en")
        start = time.time()
        result = model.transcribe(VIDEO_PATH)
        end = time.time()

        text = result["text"].strip()
        import re
        formatted = re.sub(r"([.?!])\s+", r"\1\n", text)

        with open(TRANSCRIPT_PATH, "w", encoding="utf-8") as f:
            f.write(formatted)

        print(f"Transcript saved to {TRANSCRIPT_PATH} in {round(end - start, 2)} s")
        messagebox.showinfo("Done", f"Transcript saved to {TRANSCRIPT_PATH}")
    except Exception as e:
        messagebox.showerror("Transcription Error", str(e))

# ----------------- Tkinter UI -----------------
window = tk.Tk()
window.title("LucidFrame Demo")
window.geometry("300x150")

record_btn = tk.Button(window, text="Start Recording", command=start_recording)
record_btn.pack(pady=10)

stop_btn = tk.Button(window, text="Stop Recording", command=stop_recording, state="disabled")
stop_btn.pack(pady=10)

quit_btn = tk.Button(window, text="Quit", command=window.destroy)
quit_btn.pack(pady=10)

cap = cv2.VideoCapture(0)

window.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), cv2.destroyAllWindows(), window.destroy()))
window.mainloop()