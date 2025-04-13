from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from text_extractor import extract_clean_text_from_url
from simplify_text import simplify_text
from tts import text_to_speech
import os
import uuid
import re

app = FastAPI()

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

class URLRequest(BaseModel):
    url: str
    mode: str  # "simplify", "picture_book", or "narrate"
    level: int = 8  # Default reading level

@app.post("/process-url")
async def process_url(req: URLRequest):
    raw_text = extract_clean_text_from_url(req.url)
    
    # Get the simplified text for all modes
    simplified = simplify_text(raw_text, req.level, req.mode)
    
    if req.mode == "podcast":
        # Generate unique filename for the audio
        audio_filename = f"podcast_{uuid.uuid4()}.mp3"
        audio_path = os.path.join("static", audio_filename)
        
        # Create static directory if it doesn't exist
        os.makedirs("static", exist_ok=True)
        
        # Clean up the podcast script for TTS - remove sound effects and directions
        tts_text = re.sub(r'\*\*\([^)]+\)\*\*', '', simplified)
        tts_text = re.sub(r'\*\*Host:\*\*', 'Host:', tts_text)
        
        # Generate audio from the cleaned podcast script
        try:
            audio_file = text_to_speech(tts_text, output_file=audio_path)
            
            # Verify the file exists and has content
            if audio_file and os.path.exists(audio_file) and os.path.getsize(audio_file) > 0:
                audio_url = f"/static/{audio_filename}"
                print(f"Successfully generated audio: {audio_file}, size: {os.path.getsize(audio_file)} bytes")
            else:
                print(f"Audio file generation failed or file is empty")
                audio_file = None
                audio_url = None
                
        except Exception as e:
            print(f"TTS Error: {e}")
            audio_file = None
            audio_url = None
        
        return {
            "raw": raw_text,
            "simplified": simplified,
            "audio_url": audio_url,
            "audio_path": audio_path if audio_file else None  # Include the local path for debugging
        }
    else:
        # For other modes, just return the simplified text
        return {
            "raw": raw_text,
            "simplified": simplified
        }
