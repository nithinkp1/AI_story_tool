import requests
import tempfile
from TTS.api import TTS

# Hugging Face Inference API settings
API_URL = "your-secret-api-key"
HEADERS = {"Authorization": "Bearer {HF_TOKEN}"}

def generate_story(prompt, genre, tone, length):
    full_prompt = f"Write a {length}-word {genre.lower()} story in a {tone.lower()} tone. Begin with: {prompt}"
    data = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": length + 100,  # buffer
            "temperature": 0.8,
            "do_sample": True,
            "top_p": 0.95
        }
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "generated_text" in result:
            return result["generated_text"]
        else:
            return "Error: Unexpected response format from the model."
    except Exception as e:
        return f"Error: Unable to generate story. Details: {str(e)}"

def text_to_speech(text):
    """Fast and simple Coqui TTS voice (Tacotron2-DDC)"""
    try:
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.tts_to_file(text=text, file_path=fp.name)
            return fp.name
    except Exception as e:
        return None
