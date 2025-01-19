import logging
import requests

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"  # smallest model for this usecase

def generate_with_ollama(prompt):
    """Send a request to the local Ollama server to generate a response."""
    url = f"{OLLAMA_BASE_URL}/api/generate"
    data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error connecting to Ollama: {e}")
        return "Error during summarization."

def summarize_transcription(transcription_data):
    """Summarize the transcription data text into a concise, meaningful summary using Ollama."""
    if not transcription_data:
        logging.error(f"Argument \"transcription_data\" was {transcription_data}")
        return ""

    # Concatenate all text segments into a single text block
    full_text = " ".join([entry['text'] for entry in transcription_data])

    # Define the summarization prompt
    prompt = f"Summarize the following transcription into a concise paragraph:\n\n{full_text}"

    return generate_with_ollama(prompt)
