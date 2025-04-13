from elevenlabs.client import ElevenLabs
import sys
import requests
from concurrent.futures import TimeoutError
from functools import partial
import signal
import re

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("API call timed out")

def text_to_speech(text, output_file="output.mp3", voice_id="EXAVITQu4vr4xnSDxMaL", timeout=60):
    """
    Convert text to speech with proper timeout handling
    
    Args:
        text (str): Text to convert
        output_file (str): Output file path
        voice_id (str): Voice ID to use
        timeout (int): Timeout in seconds
    """
    if not isinstance(text, str):
        try:
            text = ' '.join(list(text)) if hasattr(text, '__iter__') else str(text)
        except Exception as e:
            print(f"Error converting text to string: {e}")
            return None

    text = re.sub(r'\*\*\([^)]+\)\*\*', '', text)

    try:
        print(f"Generating speech for: {text[:50]}...")

        client = ElevenLabs(api_key="sk_7d6914011e75677178bcd9c90156a84f2a2dafaaae1ab897")
        audio = client.generate(text=text, voice=voice_id)

        # Combine generator output if needed
        if hasattr(audio, '__iter__'):
            audio_bytes = b''.join(chunk for chunk in audio if isinstance(chunk, bytes))
        else:
            audio_bytes = audio if isinstance(audio, (bytes, bytearray)) else audio.read()

        if audio_bytes and len(audio_bytes) > 100:
            with open(output_file, "wb") as f:
                f.write(audio_bytes)
            print(f"Success! Audio saved to {output_file}")
            return output_file
        else:
            print(f"Audio too small, falling back to HTTP.")
            return text_to_speech_http(text, output_file, voice_id, timeout)

    except Exception as e:
        print(f"TTS Error: {e}")
        return text_to_speech_http(text, output_file, voice_id, timeout)
    

def text_to_speech_http(text, output_file, voice_id, timeout):
    """Fallback using direct HTTP API with timeout"""
    # Ensure text is a string - handle both generator objects and other non-string types
    if not isinstance(text, str):
        try:
            # If it's an iterable/generator, convert to a list and join
            if hasattr(text, '__iter__') and not isinstance(text, (str, bytes, bytearray)):
                text = ' '.join(list(text))
            else:
                text = str(text)
        except Exception as e:
            print(f"Error converting text to string in HTTP fallback: {e}")
            return None
    
    # Remove any sound effect or formatting instructions from the text
    text = re.sub(r'\*\*\([^)]+\)\*\*', '', text)
    
    # Limit text length if needed to prevent API errors
    if len(text) > 5000:
        print(f"Text too long ({len(text)} chars), truncating to 5000 chars")
        text = text[:5000] + "..."
            
    try:
        print("Attempting direct HTTP API call to ElevenLabs...")
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": "sk_7d6914011e75677178bcd9c90156a84f2a2dafaaae1ab897",
            "Content-Type": "application/json"
        }
        data = {
            "text": text,
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            },
            "model_id": "eleven_monolingual_v1"
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # Check if we got a valid response
        if response.content and len(response.content) > 1000:  # Minimum size check
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"HTTP fallback success! Saved to {output_file}")
            return output_file
        else:
            print(f"HTTP fallback got small or empty response: {len(response.content)} bytes")
            return None
        
    except Exception as e:
        print(f"HTTP Fallback Error: {type(e).__name__}: {e}")
        # As a last resort, try a different TTS service or method here
        return None

if __name__ == "__main__":
    # Get input text
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello world! This is a test."
    
    # Run with timeout
    result = text_to_speech(text, timeout=30)
    
    if not result:
        print("Failed to generate audio")
        sys.exit(1)



"""
from elevenlabs import voices, set_api_key

set_api_key("sk_7d6914011e75677178bcd9c90156a84f2a2dafaaae1ab897")  # Replace with your actual key

for voice in voices():
    print(f"{voice.name} | {voice.voice_id} | {voice.category}")

"""
"""

from elevenlabs import generate, save, set_api_key, voices

set_api_key("sk_7d6914011e75677178bcd9c90156a84f2a2dafaaae1ab897")

for voice in voices():
    if "Sarah" in voice.name.lower():
        print(f"Use this ID: {voice.voice_id}")



audio = generate(text="Shriyan stop being so tuff", voice="EXAVITQu4vr4xnSDxMaL")  # Sarah's ID

if len(audio) < 1024:  # Check if audio is too small (less than 1KB)
    raise ValueError("Generated audio is too short - API likely failed")
save(audio, "output.mp3")
"""