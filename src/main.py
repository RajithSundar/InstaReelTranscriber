"""
Instagram Reel Speech-to-Text Transcription Tool
Main application orchestrator
"""

import sys
import time
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.url_validator import URLValidator
from src.media_extractor import MediaExtractor
from src.speech_recognizer import SpeechRecognizer
from src.cleanup_manager import auto_cleanup
# robust downloader import happens dynamically to avoid circular deps or unnecessary imports
from config import WHISPER_MODEL


# Helper to download the model if it fails
# This is needed because sometimes the connection drops
def download_model_if_needed(model_name):
    try:
        print(f"Downloading {model_name} model with resume support...")
        from src.model_downloader import download_model
        download_model(model_name)
        print("Download done! Trying to run again...")
        return True
    except Exception as e:
        print(f"Error downloading: {e}")
        return False

class InstaTranscriber:
    def __init__(self, model_name="base"):
        # Set up all our tools
        self.validator = URLValidator()
        self.extractor = MediaExtractor()
        self.recognizer = SpeechRecognizer(model_name)
        self.model_name = model_name
    
    def transcribe_reel(self, url):
        # Dictionary to store all our results
        result = {
            'success': False,
            'transcription': '',
            'reel_id': '',
            'processing_time': 0.0,
            'error': ''
        }
        
        start_time = time.time()
        
        # This auto_cleanup thing helps delete files later
        with auto_cleanup() as cleanup:
            try:
                # 1. Check if the URL is good
                print("\n" + "="*60)
                print("STEP 1: Checking URL")
                print("="*60)
                
                is_valid, reel_id, error = self.validator.validate(url)
                if not is_valid:
                    result['error'] = f"Bad URL: {error}"
                    return result
                
                result['reel_id'] = reel_id
                print(f"URL is good! ID: {reel_id}")
                
                # 2. Get the audio from the video
                print("\n" + "="*60)
                print("STEP 2: Getting Audio")
                print("="*60)
                
                success, audio_path, error = self.extractor.extract_audio(url, reel_id)
                if not success:
                    result['error'] = f"Could not get audio: {error}"
                    return result
                
                # Remember this file so we can delete it later
                cleanup.register_file(audio_path)
                
                # 3. Convert speech to text
                try:
                    print("\n" + "="*60)
                    print("STEP 3: Converting to Text")
                    print("="*60)
                    
                    # Try to transcribe
                    success, transcription, proc_time, error = self.recognizer.transcribe(audio_path)
                    
                    # If it failed because of the model, try downloading it again
                    if not success and "Failed to load Whisper model" in error:
                        print("\nModel load failed. Trying to download it properly...")
                        
                        if download_model_if_needed(self.model_name):
                            # Reset the model and try again
                            self.recognizer.model = None
                            success, transcription, proc_time, error = self.recognizer.transcribe(audio_path)
                        else:
                            result['error'] = "Model download failed."
                            return result

                    if not success:
                        result['error'] = f"Transcription broke: {error}"
                        return result
                    
                    # It worked!
                    result['success'] = True
                    result['transcription'] = transcription
                    result['processing_time'] = time.time() - start_time
                    
                    return result

                except Exception as e:
                     result['error'] = f"Something went wrong: {str(e)}"
                     return result
                
            except KeyboardInterrupt:
                result['error'] = "Stopped by user"
                return result
            except Exception as e:
               result['error'] = f"Unexpected error: {str(e)}"
               return result


def print_banner():
    """Print application banner"""
    print("\n" + "="*60)
    print("  Instagram Reel Speech-to-Text Transcription Tool")
    print("="*60)


def print_result(result: dict):
    """Print transcription result"""
    print("\n" + "="*60)
    print("RESULT")
    print("="*60)
    
    if result['success']:
        print(f"✓ Transcription completed successfully!")
        print(f"\nReel ID: {result['reel_id']}")
        print(f"Processing Time: {result['processing_time']:.2f} seconds")
        print("\n" + "-"*60)
        print("TRANSCRIPTION:")
        print("-"*60)
        print(result['transcription'])
        print("-"*60)
    else:
        print(f"✗ Transcription failed")
        print(f"\nError: {result['error']}")
    
    print()


def main():
    # Setup arguments
    parser = argparse.ArgumentParser(description='Convert Instagram Reels to Text')
    
    parser.add_argument('url', help='The Instagram URL')
    
    # Optional arguments
    parser.add_argument('-m', '--model', default=WHISPER_MODEL, 
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Which model to use (default: base)')
    
    parser.add_argument('-o', '--output', help='Save to this file')
    
    args = parser.parse_args()
    
    print_banner()
    print(f"Using Model: {args.model}")
    print(f"Processing: {args.url}")
    
    # Run the main program
    app = InstaTranscriber(model_name=args.model)
    result = app.transcribe_reel(args.url)
    
    print_result(result)
    
    # Save the file if the user asked for it
    if args.output and result['success']:
        try:
            # Make sure the folder exists
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write the text
            output_path.write_text(result['transcription'], encoding='utf-8')
            print(f"Saved to: {output_path}")
        except Exception as e:
            print(f"Could not save file: {e}")
    
    # Exit code 0 if good, 1 if bad
    if result['success']:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
