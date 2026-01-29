from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import os
import sys
from pathlib import Path

# Add parent directory to path to ensure imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import InstaTranscriber
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="InstaReelTranscriber API")

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TranscribeRequest(BaseModel):
    reel_url: str
    model: str = "base"

class TranscribeResponse(BaseModel):
    status: str
    transcription: Optional[str] = None
    message: Optional[str] = None
    reel_id: Optional[str] = None
    processing_time: Optional[float] = None

@app.post("/api/transcribe", response_model=TranscribeResponse)
async def transcribe_reel(request: TranscribeRequest, background_tasks: BackgroundTasks):
    """
    Transcribe an Instagram Reel
    """
    try:
        # Initialize transcriber with requested model
        transcriber = InstaTranscriber(model_name=request.model)
        
        # Run transcription (synchronously for now as the core logic is sync)
        # In a production app with heavy load, we'd want this to be async/queued
        result = transcriber.transcribe_reel(request.reel_url)
        
        if result['success']:
            return TranscribeResponse(
                status="success",
                transcription=result['transcription'],
                reel_id=result.get('reel_id'),
                processing_time=result.get('processing_time')
            )
        else:
            return TranscribeResponse(
                status="error",
                message=result.get('error', "Unknown error occurred")
            )
            
    except Exception as e:
        return TranscribeResponse(
            status="error",
            message=f"Server error: {str(e)}"
        )

@app.get("/health")
def health_check():
    return {"status": "healthy"}
