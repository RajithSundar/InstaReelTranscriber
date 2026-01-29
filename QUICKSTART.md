# Quick Start Guide

## Installation Steps

### 1. Install FFmpeg (Required)

**FFmpeg is REQUIRED** for this tool to work. Install it before proceeding:

**Windows (Recommended Methods):**

**Option A: Using Chocolatey (Easiest)**
```powershell
# Install Chocolatey if not already installed (run as Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install FFmpeg
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download FFmpeg from: https://www.gyan.dev/ffmpeg/builds/
2. Extract the zip file (e.g., to `C:\ffmpeg`)
3. Add to system PATH:
   - Search "Environment Variables" in Windows
   - Edit "Path" under System Variables
   - Add `C:\ffmpeg\bin` (or your installation path)
   - Restart your terminal

**Verify Installation:**
```powershell
ffmpeg -version
```

### 2. Create Virtual Environment

```powershell
# Navigate to project directory
cd d:\rajith\InstaTranscriber

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate
```

### 3. Install Python Dependencies

```powershell
# Make sure virtual environment is activated (you should see (venv) in prompt)
pip install -r requirements.txt
```

> **Note:** This will take a few minutes. The first time you run the transcription, Whisper will download its model (~1GB).

### 4. Test Installation

```powershell
# Check if main script can be loaded
python src/main.py --help
```

You should see the help menu with available options.

## Usage

### Basic Transcription

```powershell
python src/main.py "https://www.instagram.com/reel/YOUR_REEL_ID/"
```

**Example with a real public reel:**
```powershell
python src/main.py "https://www.instagram.com/reel/C5abc123xyz/"
```

### Save to File

```powershell
python src/main.py "https://www.instagram.com/reel/YOUR_REEL_ID/" --output transcript.txt
```

### Use Different Model (for better accuracy)

```powershell
python src/main.py "https://www.instagram.com/reel/YOUR_REEL_ID/" --model small
```

## Troubleshooting

### Issue: "FFmpeg not found"
✅ **Solution:** Install FFmpeg using one of the methods above, restart terminal

### Issue: "Command not recognized: python"
✅ **Solution:** Try `python3` instead, or reinstall Python from python.org

### Issue: "Permission denied" or "Access denied"
✅ **Solution:** Run PowerShell as Administrator

### Issue: "Module not found" errors
✅ **Solution:** Make sure virtual environment is activated:
```powershell
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Issue: Download fails or "Private video"
✅ **Solution:** 
- Ensure the reel is from a **public** Instagram account
- Try updating yt-dlp: `pip install --upgrade yt-dlp`
- Verify you can access the reel in your browser

### Issue: Slow transcription
✅ **Solution:**
- Use a smaller model: `--model tiny` or `--model base`
- First run is always slower (downloads model)
- Close other heavy applications

## What Happens on First Run?

1. **Model Download** (~1GB for base model)
   - Only happens once
   - Stored in `~/.cache/whisper/`
   - Takes 2-5 minutes depending on internet speed

2. **Instagram Reel Download**
   - Downloads video temporarily
   - Extracts audio
   - Files are automatically deleted after transcription

3. **Transcription**
   - Processes audio with Whisper AI
   - Typically takes 0.5-2× the video duration
   - Displays result in console

## Next Steps

- Try transcribing a short public Instagram Reel
- Experiment with different Whisper models
- Save transcriptions to files for record-keeping

## Need Help?

Check the main [README.md](README.md) for detailed documentation and examples.
