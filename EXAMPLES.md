# Example Usage Scripts

This directory contains example scripts for common use cases.

## Basic Example

**File: `basic_example.bat`**
```batch
@echo off
echo Testing Instagram Reel Transcription
python src/main.py "https://www.instagram.com/reel/YOUR_REEL_ID/"
pause
```

## Batch Processing Multiple Reels

**File: `batch_transcribe.py`**
```python
import sys
sys.path.insert(0, '..')
from src.main import InstaTranscriber

# List of Instagram Reel URLs to transcribe
reels = [
    "https://www.instagram.com/reel/REEL_ID_1/",
    "https://www.instagram.com/reel/REEL_ID_2/",
    "https://www.instagram.com/reel/REEL_ID_3/",
]

transcriber = InstaTranscriber()

for i, url in enumerate(reels, 1):
    print(f"\n{'='*60}")
    print(f" Processing Reel {i}/{len(reels)}")
    print(f"{'='*60}")
    
    result = transcriber.transcribe_reel(url)
    
    if result['success']:
        # Save to file
        filename = f"transcript_{result['reel_id']}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result['transcription'])
        print(f"✓ Saved to: {filename}")
    else:
        print(f"✗ Failed: {result['error']}")
```

## Integration with Your Python Code

```python
# Import the transcriber
import sys
sys.path.insert(0, 'path/to/InstaTranscriber')
from src.main import InstaTranscriber

# Create transcriber instance
transcriber = InstaTranscriber(model_name='base')

# Transcribe a reel
result = transcriber.transcribe_reel("https://www.instagram.com/reel/ABC123/")

# Check result
if result['success']:
    print("Transcription:", result['transcription'])
    print("Processing time:", result['processing_time'], "seconds")
else:
    print("Error:", result['error'])
```

## Custom Configuration

```python
# Create your own config
import sys
sys.path.insert(0, 'path/to/InstaTranscriber')
from src.url_validator import URLValidator
from src.media_extractor import MediaExtractor
from src.speech_recognizer import SpeechRecognizer
from src.cleanup_manager import auto_cleanup

# Use components separately
validator = URLValidator()
is_valid, reel_id, error = validator.validate(url)

if is_valid:
    with auto_cleanup() as cleanup:
        extractor = MediaExtractor()
        success, audio_path, error = extractor.extract_audio(url, reel_id)
        
        if success:
            cleanup.register_file(audio_path)
            recognizer = SpeechRecognizer(model_name='small')
            success, text, time, error = recognizer.transcribe(audio_path)
            print(text)
```
