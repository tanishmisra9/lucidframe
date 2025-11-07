# LucidFrame
### _"Record your dreams. Then watch them come to life."_

**LucidFrame** transforms your spoken or written dream journals into **AI-generated cinematic visualizations.**  

By combining language understanding, emotional analysis, and generative video models, it bridges the gap between imagination and reality — turning subconscious stories into expressive short films.

---

## Project Overview

### Vision
Everyone dreams, but few remember or visualize their dreams vividly.  
LucidFrame gives users a way to **record, preserve, and re-experience** their dreams as living art in a manner that 
doesn't feel like a chore.

You simply describe your dream — by voice, video, or text — and LucidFrame:
1. Transcribes and interprets the dream,
2. Extracts mood, imagery, and structure,
3. Generates a short AI-animated “dream film” that mirrors its tone and symbolism.

---

## Core

### MVP
- **Dream Capture**
  - Voice, video, or text journaling interface
  - Speech-to-text via Whisper / Whisper.cpp
  - Optional emotional analysis from tone of voice or expression

- **Dream Parser (LLM Layer)**
  - Uses an LLM to summarize and structure the dream into scenes:
    - _Setting, mood, key objects, transitions_
  - Generates a "dream script" with descriptive, cinematic language

- **Scene Visualization**
  - Generates a sequence of images or clips for each scene using:
    - OpenAI Image models / Stability API / RunwayML / Pika Labs
  - Applies consistent visual style (surreal, painterly, cinematic)

- **Dream Journal Dashboard**
  - Interactive web app where users can:
    - View previous dreams and their generated videos
    - See mood/emotion tags over time
    - Read AI-generated reflections or summaries

---

### Stretch Features
- **Mood Palette Generator**
  - Creates a custom color palette from the dream’s tone (e.g., “wistful,” “chaotic,” “hopeful”).

- **Dream Symbol Insight**
  - Optional “symbolic reflection” explaining recurring objects or themes (non-clinical).

- **AI Voiceover Narration**
  - Narrates your dream film in your own voice (via TTS cloning or stylized speech synthesis).

- **Dream Timeline**
  - Visual timeline showing evolution of dream themes or emotions.

- **Dream Merge Mode**
  - Combine multiple dream logs into one surreal hybrid story.

- **Collage / Poster Generator**
  - Auto-generate “dream posters” or key frames for sharing.

Supporting systems:
- 🧠 **FastAPI Backend** — coordinates transcription, LLM parsing, and media generation.
- 🪄 **React Frontend** — handles journaling, playback, and visualization.
- 🎨 **Generative Layer** — creates imagery and compiles video sequences.
- 🗄️ **Database (SQLite / MongoDB)** — stores transcripts, emotion tags, generated content.
- 🐳 **Docker Compose** — orchestrates the multi-service pipeline.

---

## Tech Stack

| Component | Tools / Frameworks | Description |
|------------|--------------------|--------------|
| **Frontend** | React / Next.js + TailwindCSS | Dream journaling dashboard, video viewer |
| **Backend** | FastAPI (Python) | API endpoints and generation pipeline |
| **Speech-to-Text** | Whisper / Whisper.cpp | Transcribe spoken dream input |
| **LLM Parsing** | GPT-4 / Mistral / Local LLM | Extract structure, scenes, and tone |
| **Emotion Analysis** | OpenSMILE / PyAudioAnalysis | Optional sentiment from voice |
| **Image / Video Gen** | RunwayML / Pika / OpenAI Image models | Generate dream visuals |
| **Video Assembly** | ffmpeg / MoviePy | Combine scenes into final clip |
| **Storage** | SQLite / S3 / Local filesystem | Store generated videos, transcripts, and metadata |
| **Visualization** | D3.js / Chart.js | Mood + trend charts for journal history |

---

## 🧑‍💻 Skills You’ll Develop

- Speech-to-text processing and transcript cleaning  
- Natural language understanding and summarization  
- Prompt-to-video generation pipelines  
- Visual consistency in generative media  
- Time-series and emotional trend visualization  
- Secure local-first storage of sensitive creative data  
- Audio emotion analysis and prosody detection  
- LLM-to-API orchestration (multi-step reasoning chain)  

---