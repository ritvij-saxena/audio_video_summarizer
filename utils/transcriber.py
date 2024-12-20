import logging
import wave
import os
import subprocess
import re
from utils.ffmpeg_helper import validate_media_duration

ffmpeg_binary_path = os.path.join("third-party", "ffmpeg", "ffmpeg")
print(f"Using ffmpeg binary at: {ffmpeg_binary_path}")
os.environ['FFMPEG_BINARY'] = ffmpeg_binary_path

def is_audio_file_supported(audio_path):
    """Check if the file is a supported audio format."""
    supported_formats = ['.mp3', '.aac', '.flac', '.ogg', '.m4a', '.wav']
    _, ext = os.path.splitext(audio_path)
    return ext.lower() in supported_formats

def convert_to_wav(audio_path):
    """Convert the given audio file to WAV format using FFmpeg."""
    output_path = os.path.splitext(audio_path)[0] + ".wav"
    try:
        subprocess.run(
            ["ffmpeg", "-i", audio_path, output_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logging.info(f"File converted to WAV: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Error converting {audio_path} to WAV: {e}")
        return None


def transcribe_audio(audio_path):
    """Transcribe audio to text using whisper.cpp."""
    logging.info(f"Transcribing audio file: {audio_path}")

    # Validate that the file is a .wav file
    if not audio_path.endswith('.wav'):
        # If not then check if it's an ffmpeg supported audio file
        if not is_audio_file_supported(audio_path):
            logging.error("Invalid file format: Supported formats are .wav, .mp3, .aac, .flac, .ogg, and .m4a")
            return None
        # If it is supported then convert "any" audio file into .wav file.
        audio_path = convert_to_wav(audio_path)
        if not audio_path:
            logging.error("Failed to convert audio file to WAV format.")
            return None

    # Checking if the duration of audio/video is less than or equal to 5 minutes
    validate_media_duration(audio_path)

    logging.info(f"Validating Sample Rate...")
    # Validate the sample rate is 16 kHz
    if not is_16khz_wav(audio_path):
        try:
            audio_path = convert_to_16khz(audio_path)
        except Exception as e:
            logging.error(f"Failed to convert audio to 16 kHz: {e}")
            return None

    # Path to the built whisper.cpp binary
    whisper_path = "third-party/whisper.cpp/main"
    model_path = "third-party/whisper.cpp/models/ggml-base.en.bin"

    logging.info("Starting Transcription")
    logging.debug(f"cmd: {whisper_path} -m {model_path} -f {audio_path}")

    result = subprocess.run(["./" + whisper_path, "-m", model_path, "-f", audio_path], capture_output=True, text=True)

    if result.returncode != 0:
        logging.error("Transcription failed: " + result.stderr)
        return None

    transcription = result.stdout.strip()

    # Validate that transcription is not empty and has time-stamped lines
    if not transcription:
        logging.error("Transcription output is empty.")
        return None

    # Define a regex to check for expected timestamped format and capture the timestamp and text
    timestamped_line_pattern = r"^\[(\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3})\]\s+(.*)"

    lines = transcription.splitlines()
    timestamped_transcription = []

    for line in lines:
        match = re.match(timestamped_line_pattern, line)
        if match:
            timestamp = match.group(1)  # Extract timestamp
            text = match.group(2)       # Extract text
            timestamped_transcription.append({"timestamp": timestamp, "text": text})
        else:
            logging.warning(f"Unexpected line format: {line}")

    # If you want to return the structured transcription (timestamp + text)
    return timestamped_transcription

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
    logging.info("Converting the audio file to 16 kHz using ffmpeg.")
    converted_path = audio_path.replace(".wav", "_16khz.wav")

    if os.path.exists(converted_path):
        logging.info(f"Removing existing file: {converted_path}")
        os.remove(converted_path)

    try:
        subprocess.run([ffmpeg_binary_path, '-i', audio_path, '-ar', '16000', converted_path], check=True)
        logging.info(f"Converted audio to 16 kHz: {converted_path}")
        return converted_path
    except subprocess.CalledProcessError as e:
        logging.error(f"ffmpeg conversion failed: {e}")
        raise RuntimeError("Failed to convert audio to 16 kHz")
