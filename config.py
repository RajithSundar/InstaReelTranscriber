# Config settings
import os
from pathlib import Path

# Main project folder
PROJECT_ROOT = Path(__file__).parent

# Where we store temporary downloads
TEMP_DIR = PROJECT_ROOT / "temp_downloads"
# Make sure the folder exists
TEMP_DIR.mkdir(exist_ok=True)

# Which Whisper model to use?
# tiny, base, small, medium, large
# "base" is a good middle ground
WHISPER_MODEL = "base"

# Audio Settings
AUDIO_FORMAT = "wav"  # Whisper works best with WAV
AUDIO_SAMPLE_RATE = 16000  # Standard for speech recognition

# Download Settings
DOWNLOAD_TIMEOUT = 300  # 5 minutes max for download
MAX_VIDEO_DURATION = 600  # 10 minutes max (Instagram reels are typically < 90 seconds)

# Performance Settings
TRANSCRIPTION_TIME_MULTIPLIER = 3  # Max allowed is 3x video duration

# Logging
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Instagram Reel URL Patterns
INSTAGRAM_REEL_PATTERN = r'https?://(?:www\.)?instagram\.com/(?:reel|reels)/([A-Za-z0-9_-]+)'

# User Agent for requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
