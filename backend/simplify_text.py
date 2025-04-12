from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key="AIzaSyADFGlfGDyraeaHUYiPTZmeGI4S3gq6QQg")

def simplify_text(text: str, level) -> str:
    prompt = (
        "Simplify the following article for a grade {level} reading level. "
        "Use simple words and short sentences. Make it friendly and easy to understand.\n\n"
        f"{text[:3000]}"  # Keep prompt under GPT token limits
    )
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=[prompt]
        )
        print(response.text.strip())
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {e}"