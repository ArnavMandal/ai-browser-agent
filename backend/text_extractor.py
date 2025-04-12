import requests
from bs4 import BeautifulSoup

def extract_clean_text_from_url(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Failed to load page: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script/style/junk tags
    for tag in soup(["script", "style", "noscript", "header", "footer", "aside", "form", "nav"]):
        tag.decompose()

    # Try to get main content
    article = soup.find("article") or soup.body
    text = article.get_text(separator="\n", strip=True)

    # Clean up: remove short junk lines
    lines = [line for line in text.splitlines() if len(line.strip()) > 40]
    return "\n".join(lines[:50])  # Limit to first ~50 lines
