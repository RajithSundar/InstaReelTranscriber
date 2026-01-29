# Instagram Reel Speech-to-Text Transcription Tool

A lightweight AI-powered tool that extracts audio from public Instagram Reels and transcribes speech into plain text using OpenAI's Whisper model.

## Features

✨ **Easy to Use**: Simple command-line interface  
🎯 **Accurate**: ~85% accuracy for clear speech using Whisper AI  
⚡ **Fast**: Transcription typically completes in ≤3× video duration  
🔒 **Privacy Focused**: Works 100% offline after initial setup  
🧹 **Clean**: Automatically deletes temporary files after processing  

## Prerequisites

### System Requirements

- **Python**: 3.8 or higher
- **FFmpeg**: Required for audio processing

### Installing FFmpeg

**Windows:**
1. Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract and add to system PATH
3. Verify: `ffmpeg -version`

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## Installation

1. **Clone or download this repository**
```bash
cd InstaTranscriber
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

> **Note**: First run will download the Whisper model (~1GB for base model). This is a one-time download.

## Usage

### Basic Usage

```bash
python src/main.py https://www.instagram.com/reel/YOUR_REEL_ID/
```

### Advanced Options

**Use a different Whisper model:**
```bash
python src/main.py https://www.instagram.com/reel/ABC123/ --model small
```

**Save transcription to file:**
```bash
python src/main.py https://www.instagram.com/reel/ABC123/ --output transcript.txt
```

**View all options:**
```bash
python src/main.py --help
```

### Whisper Model Comparison

| Model  | Size  | Speed      | Accuracy | Use Case                |
|--------|-------|------------|----------|-------------------------|
| tiny   | ~1GB  | Fastest    | Basic    | Quick tests             |
| base   | ~1GB  | Fast       | Good     | **Default - recommended** |
| small  | ~2GB  | Moderate   | Better   | Higher accuracy needed  |
| medium | ~5GB  | Slow       | High     | Professional use        |
| large  | ~10GB | Slowest    | Best     | Maximum accuracy        |

## Example Output

```
============================================================
  Instagram Reel Speech-to-Text Transcription Tool
============================================================
Model: base
URL: https://www.instagram.com/reel/ABC123/

============================================================
STEP 1: Validating Instagram Reel URL
============================================================
✓ Valid Instagram Reel URL
  Reel ID: ABC123

============================================================
STEP 2: Downloading and Extracting Audio
============================================================
Downloading Instagram Reel: ABC123...
Video duration: 30.5 seconds
✓ Audio extracted successfully

============================================================
STEP 3: Transcribing Speech to Text
============================================================
Initializing Whisper model: base
✓ Whisper model 'base' loaded successfully
Transcribing audio...
✓ Transcription completed in 15.2 seconds
  Detected language: en
  Performance ratio: 0.50x (target: ≤3x)

============================================================
RESULT
============================================================
✓ Transcription completed successfully!

Reel ID: ABC123
Processing Time: 45.7 seconds

------------------------------------------------------------
TRANSCRIPTION:
------------------------------------------------------------
Hey everyone! Today I'm going to show you how to make the
perfect cup of coffee at home. It's easier than you think!
------------------------------------------------------------

🗑️  Cleanup complete: 1 file(s) deleted
```

## Limitations

⚠️ **Instagram API Changes**: Instagram frequently updates their platform. If the tool stops working, update yt-dlp:
```bash
pip install --upgrade yt-dlp
```

⚠️ **Public Reels Only**: Only works with public Instagram Reels (not private accounts)

⚠️ **Language Support**: Best accuracy with English; other languages supported but may vary in quality

⚠️ **Background Noise**: Accuracy decreases with heavy background music or noise

## Troubleshooting

### "FFmpeg not found"
- Ensure FFmpeg is installed and in your system PATH
- Restart your terminal after installation
- Verify with: `ffmpeg -version`

### "Reel is private or not available"
- Ensure the reel is from a public account
- Verify the URL is correct
- Try accessing the reel in your browser first

### "Model download fails"
- Check your internet connection
- Ensure you have sufficient disk space (~1-10GB depending on model)
- Try a smaller model: `--model tiny`

### Slow performance
- Use a smaller model: `--model tiny` or `--model base`
- Ensure no other heavy applications are running
- Consider using a machine with better CPU/GPU

## Performance Notes

- **First run**: Slower due to model download (one-time)
- **Subsequent runs**: Much faster (~0.5-2× video duration)
- **GPU acceleration**: Automatically used if CUDA-compatible GPU detected

## Project Structure

```
InstaTranscriber/
├── src/
│   ├── __init__.py
│   ├── main.py              # Main orchestrator & CLI
│   ├── url_validator.py     # URL validation
│   ├── media_extractor.py   # Video download & audio extraction
│   ├── speech_recognizer.py # Whisper transcription
│   └── cleanup_manager.py   # Temporary file management
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## License

MIT License - feel free to use and modify as needed.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for media extraction
- [FFmpeg](https://ffmpeg.org/) for audio processing

## Future Enhancements

- 🌍 Language detection and translation
- 👥 Speaker identification
- 📊 Confidence scoring
- ⏱️ Timestamp generation
- 📱 Multi-platform support (TikTok, YouTube Shorts)

---

**Disclaimer**: This tool is for educational purposes. Respect content creators' rights and Instagram's Terms of Service. Only transcribe content you have permission to use.
