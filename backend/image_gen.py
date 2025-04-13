import requests
import uuid
from PIL import Image
from io import BytesIO
from supabase import create_client
import google.generativeai as genai

# === Gemini Config ===
GEMINI_API_KEY = "AIzaSyCpC1GhKGguCu_xa_Snm-sWunAspEo9e2s"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def get_image_prompt_from_gemini(story_text):
    gemini_prompt = (
        "Based on the following children's storybook passage, "
        "describe a visual scene that could be illustrated in cartoon style. "
        "Avoid any text, labels, or symbols in the image. Focus on people, setting, objects, and actions.\n\n"
        f"{story_text}"
    )
    try:
        response = gemini_model.generate_content(gemini_prompt)
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Gemini API error: {e}")
        return story_text  # fallback to original description

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
        "Once upon a time, in a big, tall building called the White House, lived a man named Donald. Donald loved things made in America, like juicy apples from Washington and shiny toy cars from Detroit. But he noticed that many toys in the toy shop came from far away lands, like China and Mexico.",
        """
        Donald had a big idea! "I'll put a special fee, called a tariff, on toys from other countries!" he said. "That way, people will buy more toys made right here in America!" He imagined children playing with bright red wagons and cuddly teddy bears, all made in the USA.
        """,
        """
        Soon, the toy shop started to change. The toys from far away became more expensive. A little girl named Lily wanted a beautiful doll from France, but her father said, "Oh, dear, that doll costs more now because of the special fee." Lily frowned.
        """,
        """
        A kind toy maker named Mr. Chen, who made wonderful wooden trains in China, was very sad. "It costs more to send my trains to America now," he said. "I might have to make fewer trains, and some of my friends might lose their jobs."
        """,
        """
        Some people were happy because they bought more toys made in America. But other people, like Lily and Mr. Chen, were not so happy. They learned that when things change, it can help some people but also make things harder for others. And that's a very important thing to remember.
        """
    ]

    image_urls = []

    for i, desc in enumerate(descriptions):
        print(f"\n🔄 Generating image for: {desc[:50]}")

        # Get visual-only description from Gemini
        visual_prompt = get_image_prompt_from_gemini(desc)
        print(f"🎨 Gemini visual prompt: {visual_prompt}")

        # Generate image from Gemini-generated visual prompt
        data = {"prompt": "Cartoon style illustration: " + visual_prompt}
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

# Run the full generation process
urls = generate_images_and_upload()
print("\n🖼️ Uploaded Image URLs:")
for url in urls:
    print(url)
