import requests
import uuid
from PIL import Image
from io import BytesIO
from supabase import create_client

def generate_images_and_upload():
    # === Supabase Config ===
    SUPABASE_URL = "https://rxgcxatjkgbedoajnvlr.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4Z2N4YXRqa2diZWRvYWpudmxyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ0OTM1NTQsImV4cCI6MjA2MDA2OTU1NH0.E3MqSTPRKOYAUR-VMIHAA35Shvka1WKLqC0fMUNtBXc"
    BUCKET_NAME = "storybook-images"

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    # === Clear all files from the bucket before running ===
    files = supabase.storage.from_(BUCKET_NAME).list()
    filenames = [f["name"] for f in files]
    if filenames:
        supabase.storage.from_(BUCKET_NAME).remove(filenames)
        print(f"🧼 Cleared {len(filenames)} file(s) from bucket.")
    else:
        print(f"✅ '{BUCKET_NAME}' is already empty.")

    # === ClipDrop Config ===
    CLIPDROP_API_KEY = "edb4e929c5c2cf43705efff83482e761b64859d419df2d181807006a56080e0fe5d818fdf336c45458eebb0e22bf7f5e"
    clipdrop_url = "https://clipdrop-api.co/text-to-image/v1"
    clipdrop_headers = {
        "x-api-key": CLIPDROP_API_KEY,
        "Content-Type": "application/json"
    }

    # === Prompts to Generate
    descriptions = [
        "Harold was riding a bike.",
        "A witch flew over the village at night."
    ]

    image_urls = []

    for i, desc in enumerate(descriptions):
        print(f"🔄 Generating image for: {desc[:50]}")

        # Generate image from prompt
        data = {"prompt": "Cartoon style: " + desc}
        response = requests.post(clipdrop_url, headers=clipdrop_headers, json=data)

        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            filename = f"{uuid.uuid4().hex}.png"

            # Delete file if it already exists
            try:
                supabase.storage.from_(BUCKET_NAME).remove([filename])
            except Exception:
                pass

            try:
                supabase.storage.from_(BUCKET_NAME).remove([filename])
                print(f"🧹 Removed existing file: {filename}")
            except Exception as e:
                print(f"⚠️ Skipping delete (file may not exist): {e}")

            supabase.storage.from_(BUCKET_NAME).upload(
                path=filename,
                file=buffer.getvalue(),
                file_options={"content-type": "image/png"}
            )

            print(f"✅ Uploaded: {filename}")

            # Construct public URL
            image_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
            image_urls.append(image_url)
        else:
            print(f"❌ Failed: {response.status_code} — {response.text}")

    return image_urls

urls = generate_images_and_upload()
print("\n🖼️ Uploaded Image URLs:")
for url in urls:
    print(url)
