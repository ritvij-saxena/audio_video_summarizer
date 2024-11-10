import logging
import wave
import ffmpeg
import os
import subprocess

os.environ['FFMPEG_BINARY'] = os.path.join("third-party", "ffmpeg", "ffmpeg")

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
    result = subprocess.run([whisper_path, audio_path], capture_output=True, text=True)
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
    """Convert an audio file to 16 kHz using ffmpeg-python."""
    logging.info("Converting the audio file to 16 kHz using ffmpeg-python.")
    copy_audio_path = audio_path
    logging.info("Copying and renaming audio path...")
    converted_path = copy_audio_path.replace(".wav", "_16khz.wav")

    try:
        logging.info(f"Converting audio to 16 kHz: {converted_path}")
        ffmpeg.input(audio_path).output(converted_path, ar=16000).run(overwrite_output=True)
        return converted_path
    except ffmpeg.Error as e:
        logging.error(f"ffmpeg-python conversion failed: {e.stderr.decode('utf8')}")
        raise RuntimeError("Failed to convert audio to 16 kHz")
