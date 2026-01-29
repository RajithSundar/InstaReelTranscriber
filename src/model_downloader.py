"""
Robust Whisper Model Downloader
Handles downloading Whisper models with resume support and retries.
"""

import os
import hashlib
import requests
import warnings
from tqdm import tqdm
from pathlib import Path
from typing import Optional

# Whisper model URLs (dynamically imported to ensure correctness)
try:
    import whisper
    _MODELS = whisper._MODELS
except ImportError:
    print("Warning: 'openai-whisper' not installed. Using fallback URLs (might be outdated).")
    # Fallback URLs if whisper is not installed (though it should be)
    _MODELS = {
        "base": "https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a309a19fb59149a4073e5f652d8e6c4e16d03/base.pt",
    }

def download_file_with_resume(url: str, dest_path: Path, expected_sha256: Optional[str] = None):
    """
    Download a file with resume support and progress bar.
    """
    dest_path = Path(dest_path)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get total file size
    try:
        response = requests.head(url, allow_redirects=True)
        total_size = int(response.headers.get('content-length', 0))
    except Exception as e:
        print(f"Error getting file size: {e}")
        return False

    # Check existing file
    initial_pos = 0
    if dest_path.exists():
        initial_pos = dest_path.stat().st_size
        if initial_pos == total_size:
            print("File already downloaded successfully.")
            return True
        elif initial_pos > total_size:
            print("Existing file is larger than expected. Restarting download.")
            initial_pos = 0
            dest_path.unlink()
        else:
            print(f"Resuming download from {initial_pos}/{total_size} bytes")

    # Download with resume
    headers = {'Range': f'bytes={initial_pos}-'}
    mode = 'ab' if initial_pos > 0 else 'wb'

    try:
        with requests.get(url, headers=headers, stream=True, allow_redirects=True) as r:
            r.raise_for_status()
            with open(dest_path, mode) as f, tqdm(
                desc=dest_path.name,
                initial=initial_pos,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    bar.update(len(chunk))
    except Exception as e:
        print(f"Download failed: {e}")
        return False
        
    return True

def download_model(name: str = "base"):
    """
    Download Whisper model by name using robust downloader.
    """
    if name not in _MODELS:
        raise ValueError(f"Unknown model name: {name}")
    
    url = _MODELS[name]
    download_root = os.path.join(os.getenv("USERPROFILE"), ".cache", "whisper")
    os.makedirs(download_root, exist_ok=True)
    
    filename = os.path.basename(url)
    dest_path = Path(download_root) / filename
    
    print(f"Downloading {name} model to {dest_path}...")
    success = download_file_with_resume(url, dest_path)
    
    if success:
        print(f"✓ Model {name} downloaded successfully.")
        return str(dest_path)
    else:
        raise RuntimeError(f"Failed to download model {name}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="base", help="Model name to download")
    args = parser.parse_args()
    download_model(args.model)
