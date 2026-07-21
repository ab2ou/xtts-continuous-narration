```markdown
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
   git clone [https://github.com/YOUR-USERNAME/xtts-narration-project.git](https://github.com/YOUR-USERNAME/xtts-narration-project.git)
   cd xtts-narration-project

```

2. **Install the required dependencies:**
```bash
pip install -r requirements.txt

```



---

## 🚀 Usage

Run the application locally using Python:

```bash
python app.py

```

Once running, the terminal will provide a local URL (e.g., `http://127.0.0.1:7860`) as well as a public link if sharing is enabled. Open it in your browser to start generating audio.

---

## 📁 Project Structure

```text
xtts-narration-project/
│
├── app.py              # Main application script (Gradio UI + TTS pipeline)
├── requirements.txt    # Python dependencies list
└── README.md           # Project documentation

```

---

## ⚙️ Requirements File (`requirements.txt`)

```text
TTS
gradio
torch
torchaudio
numpy
python-dotenv

```

---

## 📜 License

This project utilizes the **Coqui Public Model License (CPML)** via XTTS v2. Please review the licensing terms regarding commercial usage on the official Coqui AI repository.

```

```
