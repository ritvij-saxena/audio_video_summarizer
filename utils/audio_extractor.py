import subprocess
import os
import logging
from utils.ffmpeg_helper import validate_media_duration

# Define the path to FFmpeg binary
FFMPEG_PATH = "../third-party/ffmpeg/ffmpeg"
SUPPORTED_VIDEO_FORMATS = {".mp4", ".avi", ".mov", ".mkv", ".flv", ".webm"}  # Common video formats

def extract_audio(video_path):
    """Extract audio from a video file and save it as an audio file."""
    if not os.path.exists(video_path):
        logging.error(f"Video file not found at: {video_path}")
        return None

    # Check if video file type is supported
    if not validate_video_format(video_path):
        logging.error(f"Unsupported video format for file: {video_path}")
        return None

    # Checking if the duration of audio/video is less than or equal to 5 minutes
    validate_media_duration(video_path)

    # Generate the output audio file path
    audio_output_path = os.path.splitext(video_path)[0] + ".wav"  # Saves as an wav file

    # Run FFmpeg to extract audio
    try:
        logging.info(f"Extracting audio from: {video_path}")
        subprocess.run(["./" + FFMPEG_PATH, "-i", video_path, "-q:a", "0", "-map", "a", audio_output_path], check=True)
        logging.info(f"Audio successfully extracted to: {audio_output_path}")
        return audio_output_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to extract audio: {e}")
        return None

def validate_video_format(video_path):
    """Check if the video format is supported by FFmpeg based on the file extension."""
    _, ext = os.path.splitext(video_path)
    if ext.lower() in SUPPORTED_VIDEO_FORMATS:
        return True
    return False
