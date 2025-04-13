from google import generativeai as genai
from text_extractor import extract_clean_text_from_url

# Configure the Gemini API
genai.configure(api_key="AIzaSyDhKsqzgzDSpp6IWkUV6cEBvpBozYhtq0s")

def text_classify(url: str) -> str:
    # Ensure URL has correct schema
    if not url.startswith("http"):
        url = "https://" + url

    # Extract and clean text from the URL
    clean_text = extract_clean_text_from_url(url)

    # Send prompt to Gemini
    prompt = (
        "DO NOT ADD ANY EXTRA TEXT AT ALL. "
        "SIMPLY OUTPUT A NUMBER FROM 6-12 INDICATING THE GRADE LEVEL OF THE FOLLOWING TEXT:\n\n"
        + clean_text
    )
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)

    # Return only the response text
    return response.text.strip()

# Example usage
#print(text_classify("cnbc.com/2025/04/12/trump-exempts-phones-computers-chips-tariffs-apple-dell.html"))
