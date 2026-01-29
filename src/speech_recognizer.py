"""
Speech Recognizer Module
Transcribes audio using OpenAI Whisper
"""

import time
import whisper
from pathlib import Path
from typing import Tuple, Optional
from config import WHISPER_MODEL


class SpeechRecognizer:
    def __init__(self, model_name=WHISPER_MODEL):
        self.model_name = model_name
        self.model = None
        print(f"Using Whisper model: {model_name}")
    
    def load_model(self):
        # Load the model into memory
        try:
            self.model = whisper.load_model(self.model_name)
            print(f"Model loaded!")
            return True
        except Exception as e:
            print(f"Model load failed: {e}")
            return False
    
    def transcribe(self, audio_path, expected_duration=None):
        # First make sure model is loaded
        if self.model is None:
            if not self.load_model():
                return False, "", 0.0, "Failed to load Whisper model"
        
        if not Path(audio_path).exists():
            return False, "", 0.0, f"File missing: {audio_path}"
        
        try:
            print(f"Transcribing: {audio_path}")
            start_time = time.time()
            
            # Do the magic
            result = self.model.transcribe(
                audio_path,
                fp16=False, # Use standard precision
                language=None, # Auto-detect
                verbose=False
            )
            
            processing_time = time.time() - start_time
            transcription = result["text"].strip()
            detected_language = result.get("language", "unknown")
            
            print(f"Done in {processing_time:.2f} seconds")
            print(f"Language: {detected_language}")
            
            if not transcription:
                return False, "", processing_time, "No speech found"
            
            return True, transcription, processing_time, ""
            
        except RuntimeError as e:
            error_msg = str(e)
            if "CUDA" in error_msg:
                return False, "", 0.0, "GPU error - try CPU"
            else:
                return False, "", 0.0, f"Runtime error: {error_msg}"
                
        except Exception as e:
            return False, "", 0.0, f"Error: {str(e)}"


# Helper function
def transcribe_audio(audio_path, model_name=WHISPER_MODEL):
    recognizer = SpeechRecognizer(model_name)
    return recognizer.transcribe(audio_path)
