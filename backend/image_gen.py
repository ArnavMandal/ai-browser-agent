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

# === Supabase Config ===
SUPABASE_URL = "https://rxgcxatjkgbedoajnvlr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4Z2N4YXRqa2diZWRvYWpudmxyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ0OTM1NTQsImV4cCI6MjA2MDA2OTU1NH0.E3MqSTPRKOYAUR-VMIHAA35Shvka1WKLqC0fMUNtBXc"
BUCKET_NAME = "storybook-images"

# === ClipDrop Config ===
CLIPDROP_API_KEY = "f2119d60a9a701a972c0fe6d0e06b572263cceaa8c01c1bae4c8677f1140d2304f889f0b8d5e8a81ea77a3b5f5867244"
clipdrop_url = "https://clipdrop-api.co/text-to-image/v1"
clipdrop_headers = {
    "x-api-key": CLIPDROP_API_KEY,
    "Content-Type": "application/json"
}

def get_image_prompt_from_gemini(story_text):
    """Generate a visual scene description for image generation based on text"""
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

def init_supabase():
    """Initialize and return a Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def clear_bucket(supabase, bucket_name=BUCKET_NAME):
    """Clear all files from a Supabase storage bucket"""
    files = supabase.storage.from_(bucket_name).list()
    filenames = [f["name"] for f in files]
    if filenames:
        supabase.storage.from_(bucket_name).remove(filenames)
        print(f"🧼 Cleared {len(filenames)} file(s) from bucket.")
    else:
        print(f"✅ '{bucket_name}' is already empty.")

def generate_image_from_text(text):
    """Generate a single image from text and return the image data"""
    # Get visual-only description from Gemini
    visual_prompt = get_image_prompt_from_gemini(text)
    print(f"🎨 Gemini visual prompt: {visual_prompt}")

    # Generate image from Gemini-generated visual prompt
    data = {"prompt": "Cartoon style illustration: " + visual_prompt}
    response = requests.post(clipdrop_url, headers=clipdrop_headers, json=data)

    if response.status_code == 200:
        return response.content
    else:
        print(f"❌ Failed: {response.status_code} — {response.text}")
        return None

def upload_image_to_supabase(image_data, supabase=None):
    """Upload an image to Supabase storage and return the URL"""
    if supabase is None:
        supabase = init_supabase()
        
    if image_data is None:
        return None
        
    # Process image data
    image = Image.open(BytesIO(image_data))
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    filename = f"{uuid.uuid4().hex}.png"

    # Try to remove file if it exists (ignoring errors)
    try:
        supabase.storage.from_(BUCKET_NAME).remove([filename])
    except Exception:
        pass

    # Upload the file
    supabase.storage.from_(BUCKET_NAME).upload(
        path=filename,
        file=buffer.getvalue(),
        file_options={"content-type": "image/png"}
    )

    print(f"✅ Uploaded: {filename}")

    # Construct public URL
    image_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
    return image_url

def generate_storybook_images(story_sections):
    """
    Generate images for each section of a storybook
    
    Args:
        story_sections (list): List of text sections for the storybook
        
    Returns:
        list: List of image URLs
    """
    print(f"Generating images for {len(story_sections)} storybook sections")
    
    supabase = init_supabase()
    image_urls = []
    
    for i, section in enumerate(story_sections):
        print(f"\n🔄 Generating image for section {i+1}: {section[:50]}...")
        
        # Generate and upload image
        image_data = generate_image_from_text(section)
        if image_data:
            url = upload_image_to_supabase(image_data, supabase)
            if url:
                image_urls.append(url)
    
    return image_urls

