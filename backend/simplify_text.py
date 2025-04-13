from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key="AIzaSyADFGlfGDyraeaHUYiPTZmeGI4S3gq6QQg")

def simplify_text(text: str, level, type="simplify") -> str:
    prompt_input = create_prompt(text, level, type)
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=[prompt_input]
        )
        print(response.text.strip())
        return response.text.strip()
    except Exception as e:
        return f"Error generating response: {e}"

def create_prompt(text, level, type):
    if (type == "simplify"):
        return (
            f"Simplify the following article for a {level}th-grade reading level while keeping similar length. "
            "Make it friendly and easy to understand.\n\n"
            f"{text}"  # Keep prompt under GPT token limits
        )
    elif (type == "picture_book"):
        return (
            "Rewrite the following article as a picture book for children. Make it into 5 short sections, with three questions marks in between each section (???)"
            "Use simple words and short sentences. Make it engaging.\n\n"
            f"{text[:5000]}"
        )
    elif (type == "podcast"):
        return (
            "Rewrite the following article as a podcast script without queues in it."
            "Make it engaging.\n\n"
            f"{text[:5000]}"
        )
    elif (type == "quiz"):
        return (
            "Create a quiz based on the following article. "
            "Include 5 questions with 4 multiple choice answers each. "
            "Make it engaging.\n\n"
            f"{text[:5000]}"
        )