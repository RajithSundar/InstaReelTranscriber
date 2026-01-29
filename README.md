# 🎙️ Instagram Reel Speech-to-Text Transcription Tool

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

A lightweight, privacy-focused tool that extracts audio from public Instagram Reels and transcribes speech into plain text using OpenAI's Whisper model.

---

## 📖 Table of Contents
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features

- **🎯 Accurate**: ~95% accuracy for clear speech using OpenAI's Whisper AI
- **⚡ Fast**: Transcription typically completes in < 30% of video duration (after initial setup)
- **🔒 Privacy Focused**: Works 100% offline after model download
- **🧹 Clean**: Automatically handles cleanup of temporary audio files
- **🖥️ Cross-Platform**: Windows, macOS, and Linux support
- **🕸️ Web Interface**: Beautiful, modern web UI included

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/RajithSundar/InstaTranscriber.git
cd InstaTranscriber

# Install
pip install -r requirements.txt

# Run
python src/main.py https://www.instagram.com/reel/YOUR_REEL_ID/
```

> **Note:** The first run will automatically download a ~1GB Whisper model.

---

## 🕸️ Web Interface (New!)

InstaTranscriber now includes a modern web interface.

### 1. Start the Backend API
```bash
uvicorn src.api:app --reload
```

### 2. Start the Frontend
In a new terminal:
```bash
cd frontend
npm run dev
```

### 3. Open in Browser
Visit [http://localhost:3000](http://localhost:3000) to use the tool.

---

## 🛠️ Installation

### 1. Prerequisites
- **Python 3.8+**
- **FFmpeg**: Required for audio processing.

<details>
<summary><b>Click to expand FFmpeg Installation Guide</b></summary>

**Windows:**
1. Download from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract and add `bin` folder to system PATH
3. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update && sudo apt install ffmpeg
```
</details>

### 2. Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 💻 Usage

### Basic Transcription
```bash
python src/main.py https://www.instagram.com/reel/C-xyz123/
```

### Advanced Options

| Option | Description | Example |
|--------|-------------|---------|
| `--model` | Choose model size (tiny, base, small, medium, large) | `--model small` |
| `--output` | Save to a text file | `--output result.txt` |
| `--help` | Show all available options | `--help` |

### Model Selection Guide

| Model | VRAM/RAM | Speed | Accuracy | Best For |
|-------|----------|-------|----------|----------|
| `tiny` | ~1 GB | ⚡⚡⚡ | Passable | Quick debugging |
| `base` | ~1 GB | ⚡⚡ | Good | **General Purpose (Default)** |
| `small` | ~2 GB | ⚡ | Better | Clearer speech |
| `medium`| ~5 GB | 🐢 | High | Complex audio |
| `large` | ~10 GB | 🐢🐢 | Highest | Professional results |

---

## 📝 Example Output

<details>
<summary><b>View Terminal Output</b></summary>

```text
============================================================
  Instagram Reel Speech-to-Text Transcription Tool
============================================================
Model: base
URL: https://www.instagram.com/reel/ABC123/

STEP 1: Validating Instagram Reel URL
✓ Valid Instagram Reel URL (ID: ABC123)

STEP 2: Downloading and Extracting Audio
Downloading...
✓ Audio extracted successfully

STEP 3: Transcribing Speech to Text
Initializing Whisper model: base
✓ Model loaded
✓ Transcription completed in 15.2s

============================================================
RESULT
============================================================
TRANSCRIPTION:
------------------------------------------------------------
Hey everyone! Today I'm going to show you how to make the
perfect cup of coffee at home. It's easier than you think!
------------------------------------------------------------
```
</details>

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| **FFmpeg not found** | Ensure FFmpeg is in your system PATH and restart terminal. |
| **Model download fails** | Check internet connection and disk space (~1-3GB needed). |
| **Reel not found** | The reel must be **public**. Private accounts are not supported. |
| **Slow transcription** | Try `--model tiny` for faster results on older hardware. |

---

## 📂 Project Structure

```bash
InstaTranscriber/
├── src/
│   ├── main.py              # CLI Entry point
│   ├── media_extractor.py   # Download & Audio extraction
│   ├── speech_recognizer.py # Whisper AI Logic
│   └── ...
├── config.py                # Global settings
└── requirements.txt         # Dependencies
```

---

## 📜 License

This project is licensed under the MIT License.
**Disclaimer**: Use responsibly. Respect all copyright and privacy laws.
