import logging
import subprocess

def transcribe_audio(audio_path):
    """Transcribe audio to text using whisper.cpp."""
    logging.info(f"Transcribing audio file: {audio_path}")
    whisper_path = "./third-party/whisper.cpp/main"  # Path to the built whisper.cpp binary
    """
    To run the command use ../../ <path>
    """
    result = subprocess.run([whisper_path, audio_path], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error("Transcription failed: " + result.stderr)
        return None
    return result.stdout
