import requests
from PIL import Image
from io import BytesIO

API_KEY = "edb4e929c5c2cf43705efff83482e761b64859d419df2d181807006a56080e0fe5d818fdf336c45458eebb0e22bf7f5e"  # Replace this
url = "https://clipdrop-api.co/text-to-image/v1"
headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json"
}

# List of descriptions (you can add more than 5, it will stop at 5)
descriptions = [
    "King Leo built shiny gates called tariffs to protect his kingdom’s toys.",
    "The villagers were puzzled why their favorite toys were now so expensive.",
    "Local toymakers cheered while the merchants scratched their heads.",
    "Queen Lina opened the gates for friendly traders from the south.",
    "The kingdom found balance and learned the magic of smart trading."
]

# Process only the first 5 descriptions
for i, desc in enumerate(descriptions[:5]):
    prompt = (
        "Cartoon Style:" + desc
    )
    data = {"prompt": prompt}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image.show()
        print(f"✅ Displayed image {i+1}")
    else:
        print(f"❌ Failed to generate image {i+1} — {response.status_code}: {response.text}")
