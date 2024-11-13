import subprocess
import os
import logging

# Define the path to FFmpeg binary
FFMPEG_PATH = "third-party/ffmpeg/ffmpeg"

def extract_audio(video_path):
    """Extract audio from a video file and save it as an audio file."""
    if not os.path.exists(video_path):
        logging.error(f"Video file not found at: {video_path}")
        return None

    # Generate the output audio file path
    audio_output_path = os.path.splitext(video_path)[0] + ".mp3"  # Saves as an mp3 file

    # Run FFmpeg to extract audio
    try:
        logging.info(f"Extracting audio from: {video_path}")
        subprocess.run(["./" + FFMPEG_PATH, "-i", video_path, "-q:a", "0", "-map", "a", audio_output_path], check=True)
        logging.info(f"Audio successfully extracted to: {audio_output_path}")
        return audio_output_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to extract audio: {e}")
        return None
