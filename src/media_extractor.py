"""
Media Extractor Module
Downloads Instagram Reels and extracts audio using yt-dlp
"""

import os
import subprocess
from pathlib import Path
from typing import Optional, Tuple
import yt_dlp
from config import TEMP_DIR, AUDIO_FORMAT, AUDIO_SAMPLE_RATE, DOWNLOAD_TIMEOUT


class MediaExtractor:
    def __init__(self, temp_dir=TEMP_DIR):
        # Create temp folder if it doesn't exist
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(exist_ok=True)
        self.downloaded_files = []
    
    def extract_audio(self, url, reel_id):
        
        # We'll save it as a wav file
        audio_filename = f"{reel_id}.{AUDIO_FORMAT}"
        audio_path = self.temp_dir / audio_filename
        
        # Settings for yt-dlp to download and convert to audio
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(self.temp_dir / f'{reel_id}.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'extract_audio': True, # We only want audio
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': AUDIO_FORMAT,
                'preferredquality': '192',
            }],
            'postprocessor_args': [
                '-ar', str(AUDIO_SAMPLE_RATE)
            ],
            'socket_timeout': DOWNLOAD_TIMEOUT,
            'retries': 3,
            # Pretend to be a browser so Instagram doesn't block us
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        }
        
        try:
            # Do the download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading Reel: {reel_id}...")
                info = ydl.extract_info(url, download=True)
                
                # Check how long the video is
                duration = info.get('duration', 0)
                print(f"Video length: {duration:.1f} seconds")
            
            # Make sure it actually worked
            if not audio_path.exists():
                return False, "", f"File not found at {audio_path}"
            
            # Keep track so we can delete later
            self.downloaded_files.append(str(audio_path))
            
            print(f"Audio ready: {audio_path}")
            return True, str(audio_path), ""
            
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            if "Private video" in error_msg:
                return False, "", "Video is private!"
            elif "Video unavailable" in error_msg:
                return False, "", "Video deleted or missing"
            else:
                return False, "", f"Download error: {error_msg}"
                
        except Exception as e:
            return False, "", f"Something broke: {str(e)}"
    
    def get_downloaded_files(self):
        return self.downloaded_files


# Helper function
def extract_audio_from_reel(url, reel_id):
    extractor = MediaExtractor()
    return extractor.extract_audio(url, reel_id)
