import logging
import wave
import ffmpeg
import os
import subprocess

ffmpeg_binary_path = os.path.join("third-party", "ffmpeg", "ffmpeg")
print(f"Using ffmpeg binary at: {ffmpeg_binary_path}")
os.environ['FFMPEG_BINARY'] = ffmpeg_binary_path

def transcribe_audio(audio_path):
    """Transcribe audio to text using whisper.cpp."""
    logging.info(f"Transcribing audio file: {audio_path}")

    # Validate that the file is a .wav file
    if not audio_path.endswith('.wav'):
        logging.error("Invalid file format: Only .wav files are supported.")
        return None

    logging.info(f"Validating Sample Rate...")
    # Validate the sample rate is 16 kHz
    if not is_16khz_wav(audio_path):
        try:
            audio_path = convert_to_16khz(audio_path)
        except Exception as e:
            logging.error(f"Failed to convert audio to 16 kHz: {e}")
            return None

    # Path to the built whisper.cpp binary
    whisper_path = "./third-party/whisper.cpp/main"
    result = subprocess.run([whisper_path, "-f", audio_path], capture_output=True, text=True)
    if result.returncode != 0:
        logging.error("Transcription failed: " + result.stderr)
        return None
    return result.stdout

def is_16khz_wav(audio_path):
    """Check if a .wav file has a 16 kHz sampling rate."""
    logging.info(f"Checking if a .wav file has a 16 kHz sampling rate.")
    try:
        with wave.open(audio_path, 'rb') as wav_file:
            sample_rate = wav_file.getframerate()
            logging.info(f"Current Sample Rate: {sample_rate}")
            return sample_rate == 16000
    except wave.Error as e:
        logging.error(f"Error reading .wav file: {e}")
        logging.error(f"Error: {e}")
        return False

def convert_to_16khz(audio_path):
    """Convert an audio file to 16 kHz using ffmpeg."""
    converted_path = audio_path.replace(".wav", "_16khz.wav")
    ffmpeg_binary_path = os.path.join("third-party", "ffmpeg", "ffmpeg")

    try:
        subprocess.run([ffmpeg_binary_path, '-i', audio_path, '-ar', '16000', converted_path], check=True)
        print(f"Converted audio to 16 kHz: {converted_path}")
        return converted_path
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg conversion failed: {e}")
        raise RuntimeError("Failed to convert audio to 16 kHz")
