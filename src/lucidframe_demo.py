import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import threading
import subprocess
import os
import whisper
import re
import warnings

VIDEO_PATH = "tests/video.mp4"
TRANSCRIPT_PATH = "tests/transcript.txt"
DEVICE = "0:1"
MODEL = "turbo"  # can change this to use different Whisper models

# Suppress Python warnings for cleaner console output
warnings.filterwarnings("ignore")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class VideoRecorder:
    def __init__(self):
        self.recording = False
        self.ffmpeg_proc = None
        self.cap = cv2.VideoCapture(0)
        self.model = None
        
        # Get actual webcam dimensions
        self.cam_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.cam_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Calculate display size (scale down if needed, maintain aspect ratio)
        max_width = 960
        max_height = 720
        scale = min(max_width / self.cam_width, max_height / self.cam_height, 1.0)
        self.display_width = int(self.cam_width * scale)
        self.display_height = int(self.cam_height * scale)
        
    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.display_width, self.display_height))
            img = ImageTk.PhotoImage(image=Image.fromarray(frame))
            video_label.config(image=img)
            video_label.image = img
        window.after(10, self.show_frame)
    
    def start_recording(self):
        os.makedirs("tests", exist_ok=True)
        cmd = [
            "ffmpeg", "-f", "avfoundation", "-framerate", "30",
            "-video_size", "1280x720", "-i", DEVICE,
            "-thread_queue_size", "512", "-use_wallclock_as_timestamps", "1",
            "-vsync", "1", "-async", "1", "-pix_fmt", "yuv420p",
            "-c:v", "libx264", "-preset", "ultrafast", "-c:a", "aac",
            "-shortest", "-y", VIDEO_PATH,
            "-loglevel", "error"  # Suppress FFmpeg verbose output
        ]
        try:
            # Redirect FFmpeg stdout/stderr to suppress console spam
            self.ffmpeg_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.recording = True
            record_btn.config(state="disabled")
            stop_btn.config(state="normal")
            print("Recording started")
        except Exception as e:
            messagebox.showerror("Error", f"Could not start recording:\n{e}")
    
    def stop_recording(self):
        self.recording = False
        if self.ffmpeg_proc:
            self.ffmpeg_proc.terminate()
            self.ffmpeg_proc.wait()
        stop_btn.config(text="Transcribing...", state="disabled")
        print("Recording stopped")
        threading.Thread(target=self.transcribe_and_quit, daemon=True).start()
    
    def transcribe_and_quit(self):
        try:
            if not os.path.exists(VIDEO_PATH):
                messagebox.showerror("Error", "No recorded video found.")
                self.cleanup()
                return
            
            print(f"Transcribing with Whisper {MODEL}...")
            if not self.model:
                self.model = whisper.load_model(MODEL)
            
            # fp16=False prevents "FP16 not supported on CPU" warning
            result = self.model.transcribe(VIDEO_PATH, fp16=False)
            formatted = re.sub(r"([.?!])\s+", r"\1\n", result["text"].strip())
            
            with open(TRANSCRIPT_PATH, "w", encoding="utf-8") as f:
                f.write(formatted)
            
            print(f"Transcript saved to {TRANSCRIPT_PATH}")
        except Exception as e:
            messagebox.showerror("Transcription Error", str(e))
        finally:
            self.cleanup()
    
    def cleanup(self):
        self.cap.release()
        window.destroy()

# UI Setup
recorder = VideoRecorder()
window = tk.Tk()
window.title("LucidFrame Demo")
window.geometry(f"{recorder.display_width}x{recorder.display_height + 80}")
window.resizable(False, False)

# Video feed
video_label = tk.Label(window, bg="black", width=recorder.display_width, height=recorder.display_height)
video_label.pack(fill=tk.BOTH, expand=True)

# Button frame
button_frame = tk.Frame(window)
button_frame.pack(fill=tk.X, pady=10)

record_btn = tk.Button(button_frame, text="Start Recording", command=recorder.start_recording, 
                       font=("Arial", 12), width=15)
record_btn.pack(side=tk.LEFT, padx=(recorder.display_width//2 - 170, 10))

stop_btn = tk.Button(button_frame, text="Stop & Quit", command=recorder.stop_recording, 
                     font=("Arial", 12), width=15, state="disabled")
stop_btn.pack(side=tk.LEFT, padx=10)

window.protocol("WM_DELETE_WINDOW", recorder.cleanup)
recorder.show_frame()
window.mainloop()