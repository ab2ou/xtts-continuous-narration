# XTTS v2 Continuous Narration Pipeline

A Python-based application built with **Gradio** and **Coqui TTS (XTTS v2)** designed for high-quality, long-form continuous voice cloning and narration. It automatically cleans reference audio, splits long text into manageable chunks, generates speech sequentially, and applies smooth cross-fading to merge the audio pieces seamlessly.

## ✨ Features

* **Voice Cloning:** Clone any voice using a short reference audio sample (WAV).
* **Smart Text Chunking:** Automatically splits long texts into sentence-based chunks to prevent generation limits or artifacts.
* **Audio Preprocessing:** Uses FFmpeg to filter frequencies (highpass/lowpass) and remove silence from the reference audio.
* **Seamless Audio Merging:** Applies micro fade-in and fade-out effects between chunks to ensure a natural flow.
* **Gradio Web UI:** Provides an easy-to-use graphical interface with language and text inputs.

---

## 📋 Prerequisites

Before running the project, make sure you have the following installed on your system:

1. **Python 3.10+**
2. **FFmpeg**: Required for audio processing and cleaning.
   * *Ubuntu/Debian:* `sudo apt install ffmpeg`
   * *macOS:* `brew install ffmpeg`
   * *Windows:* Download from the official FFmpeg site and add it to your System PATH.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone (https://github.com/ab2ou/xtts-continuous-narration.git)
   cd xtts-narration-project
