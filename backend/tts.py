from elevenlabs.client import ElevenLabs
import sys
import requests
from concurrent.futures import TimeoutError
from functools import partial
import signal

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("API call timed out")

def text_to_speech(text, output_file="output.mp3", voice_id="EXAVITQu4vr4xnSDxMaL", timeout=30):
    """
    Convert text to speech with proper timeout handling
    
    Args:
        text (str): Text to convert
        output_file (str): Output file path
        voice_id (str): Voice ID to use
        timeout (int): Timeout in seconds
    """
    client = ElevenLabs(api_key="sk_7d6914011e75677178bcd9c90156a84f2a2dafaaae1ab897")
    
    # Set up timeout handler
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    
    try:
        print(f"Generating speech for: {text[:50]}...")
        
        try:
            # Generate audio with timeout protection
            audio = client.generate(
                text=text,
                voice=voice_id
            )
            
            with open(output_file, "wb") as f:
                f.write(audio)
            print(f"Success! Audio saved to {output_file}")
            return output_file
            
        except TimeoutException:
            print(f"Timeout after {timeout} seconds - switching to HTTP API")
            return text_to_speech_http(text, output_file, voice_id, timeout)
            
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")
            return None
            
    finally:
        # Disable the alarm
        signal.alarm(0)

def text_to_speech_http(text, output_file, voice_id, timeout):
    """Fallback using direct HTTP API with timeout"""
    try:
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
            }
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"HTTP fallback success! Saved to {output_file}")
        return output_file
        
    except Exception as e:
        print(f"HTTP Fallback Error: {type(e).__name__}: {e}")
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