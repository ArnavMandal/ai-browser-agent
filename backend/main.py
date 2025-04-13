from fastapi import FastAPI
from pydantic import BaseModel
from text_extractor import extract_clean_text_from_url
from simplify_text import simplify_text
from tts import text_to_speech
import os
import uuid

app = FastAPI()

class URLRequest(BaseModel):
    url: str
    mode: str  # "simplify", "picture_book", or "narrate"
    level: int = 8  # Default reading level

@app.post("/process-url")
async def process_url(req: URLRequest):
    raw_text = extract_clean_text_from_url(req.url)
    
    if req.mode == "podcast":
        # Generate unique filename for the audio
        audio_filename = f"podcast_{uuid.uuid4()}.mp3"
        audio_path = os.path.join("static", audio_filename)
        
        # Create static directory if it doesn't exist
        os.makedirs("static", exist_ok=True)
        
        # Generate audio
        audio_file = text_to_speech(raw_text, output_file=audio_path)
        
        # Get the simplified text
        simplified = simplify_text(raw_text, req.level, req.mode)
        
        return {
            "raw": raw_text,
            "simplified": simplified,
            "audio_url": f"/static/{audio_filename}" if audio_file else None
        }
    else:
        # For other modes, just return the simplified text
        simplified = simplify_text(raw_text, req.level, req.mode)
        return {
            "raw": raw_text,
            "simplified": simplified
        }
