from fastapi import FastAPI
from pydantic import BaseModel
from text_extractor import extract_clean_text_from_url
from simplify_text import simplify_text

app = FastAPI()

class URLRequest(BaseModel):
    url: str
    mode: str  # "simplify", "picture_book", or "narrate"

@app.post("/process-url")
async def process_url(req: URLRequest):
    raw_text = extract_clean_text_from_url(req.url)
    # Simplify it (placeholder)
    simplified = simplify_text(raw_text, 5, req.mode)
    #reading
    return {
        "raw": raw_text,
        "simplified": simplified,
    }
