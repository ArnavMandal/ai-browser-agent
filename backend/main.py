from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from text_extractor import extract_clean_text_from_url
from simplify_text import simplify_text
from image_gen import generate_storybook_images
from tts import text_to_speech
import os
import uuid
import re

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

class URLRequest(BaseModel):
    url: str
    mode: str  # "simplify", "picture_book", "podcast", "quiz"
    level: int = 8  # Default reading level

@app.post("/process-url")
async def process_url(req: URLRequest):
    raw_text = extract_clean_text_from_url(req.url)
    
    # Get the simplified text for all modes
    simplified = simplify_text(raw_text, req.level, req.mode)
    #urls = generate_images_and_upload(simplified)
    

    #return {
    #    "raw": raw_text,
    #    "simplified": simplified,
    #}
    
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
        except Exception as e:
            print(f"TTS Error: {e}")
            audio_file = None
        
        # Create a full URL for the audio file
        audio_url = f"/static/{audio_filename}" if audio_file else None
        
        return {
            "raw": raw_text,
            "simplified": simplified,
            "audio_url": audio_url,
            "audio_path": audio_path if audio_file else None  # Include the local path for debugging
        }
    elif req.mode == "picture_book":
        # Split the story into sections (marked by "???")
        story_sections = simplified.split("???")
        story_sections = [section.strip() for section in story_sections if section.strip()]
        
        # Generate images for each section
        image_urls = generate_storybook_images(story_sections)
        
        # Create a combined response with text sections and images
        storybook_sections = []
        for i, section in enumerate(story_sections):
            image_url = image_urls[i] if i < len(image_urls) else None
            storybook_sections.append({
                "text": section,
                "image_url": image_url
            })
        
        return {
            "raw": raw_text,
            "simplified": simplified,
            "storybook_sections": storybook_sections
        }
    else:
        # For other modes, just return the simplified text
        return {
            "raw": raw_text,
            "simplified": simplified
        }
