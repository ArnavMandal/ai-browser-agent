import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_clean_text_from_url(url: str) -> str:
    try:
        logger.info(f"Attempting to fetch URL: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info("Successfully fetched the URL")
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The website took too long to respond."
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to the website. Please check your internet connection."
    except requests.exceptions.HTTPError as e:
        return f"Error: The website returned an error: {e.response.status_code}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

    try:
        soup = BeautifulSoup(response.text, "html.parser")
        logger.info("Successfully parsed HTML content")

        # Remove script/style/junk tags
        for tag in soup(["script", "style", "noscript", "header", "footer", "aside", "form", "nav"]):
            tag.decompose()

        # Try to get main content
        article = soup.find("article") or soup.body
        if not article:
            return "Error: Could not find main content on the page."
            
        text = article.get_text(separator="\n", strip=True)

        # Clean up: remove short junk lines
        lines = [line for line in text.splitlines() if len(line.strip()) > 40]
        if not lines:
            return "Error: No readable content found on the page."
            
        return "\n".join(lines[:50])  # Limit to first ~50 lines
    except Exception as e:
        logger.error(f"Error processing content: {str(e)}")
        return f"Error: Failed to process the page content: {str(e)}"
