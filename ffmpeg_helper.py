#!/usr/bin/env python3

import logging
import subprocess
import os

# Paths
FFMPEG_PATH = "third-party/ffmpeg/ffmpeg"
FFMPEG_REPO_URL = "https://git.ffmpeg.org/ffmpeg.git"
FFMPEG_SOURCE_PATH = "third-party/ffmpeg"
DOWNLOAD_URL = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz"  # Example URL for precompiled binary


def ensure_ffmpeg():
    """Ensure FFmpeg is installed and working."""
    if check_ffmpeg():
        logging.info("FFmpeg is already installed and working.")
        return True

    logging.info("FFmpeg is not installed or not working.")

    # Attempt to build FFmpeg from source
    if build_ffmpeg():
        return True

    logging.error("FFmpeg installation or build failed.")
    return False

def check_ffmpeg():
    """Check if the FFmpeg binary exists and works."""
    logging.info("Checking if the FFmpeg binary exists and works.")
    if os.path.exists(FFMPEG_PATH):
        try:
            subprocess.run(["./" + FFMPEG_PATH, "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logging.info("FFmpeg binary is found and working.")
            return True
        except subprocess.CalledProcessError:
            logging.error("FFmpeg binary is found but not working.")
            return False
    logging.error("FFmpeg binary not found.")
    return False


def build_ffmpeg():
    """Run ./configure, make, and then set executable permissions for FFmpeg."""
    logging.info("FFmpeg binary not found. Attempting to build from source...")
    try:
        # Step 1: Clone the FFmpeg repository if it's not already cloned
        if not os.path.exists(FFMPEG_SOURCE_PATH):
            subprocess.run(["git", "clone", FFMPEG_REPO_URL, FFMPEG_SOURCE_PATH], check=True)

        # Step 2: Change to the FFmpeg directory
        os.chdir(FFMPEG_SOURCE_PATH)

        # Step 3: Run ./configure
        logging.info("Running ./configure...")
        subprocess.run(["./configure"], check=True)

        # Step 4: Build FFmpeg using make
        logging.info("Building FFmpeg with make...")
        subprocess.run(["make"], check=True)

        # Step 5: Ensure the FFmpeg binary exists
        if not os.path.exists("ffmpeg"):
            logging.error("FFmpeg binary not found after build.")
            return False

        # Step 6: Set executable permissions for the binary
        if not set_executable_permissions():
            return False

        # Step 7: Validate FFmpeg works after building
        if not check_ffmpeg():
            logging.error("FFmpeg build completed, but the binary is still not working.")
            return False

        logging.info("FFmpeg built successfully and is working.")
        os.chdir("../../")  # Return to the original directory
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"Error during FFmpeg build process: {e}")
        return False


def set_executable_permissions():
    """Ensure the FFmpeg binary has executable permissions."""
    try:
        logging.info("Setting executable permissions for the FFmpeg binary...")
        subprocess.run(["chmod", "+x", FFMPEG_PATH], check=True)
        logging.info(f"Set executable permissions for {FFMPEG_PATH}.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error setting executable permissions for {FFMPEG_PATH}: {e}")
        return False

def get_media_duration(file_path):
    """Get the duration of the media file using ffmpeg."""
    try:
        result = subprocess.run(
            ['./third-party/ffmpeg/ffmpeg', '-i', file_path],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        # Search for the duration in the output
        for line in result.stderr.split('\n'):
            if 'Duration' in line:
                # Duration format: Duration: 00:03:59.99 (example)
                duration_str = line.split('Duration: ')[1].split(',')[0]
                hours, minutes, seconds = map(float, duration_str.split(':'))
                total_seconds = hours * 3600 + minutes * 60 + seconds
                return total_seconds
        raise ValueError("Duration not found in the file")

    except Exception as e:
        logging.error(f"Error extracting media duration: {e}")
        return None

def validate_media_duration(file_path, max_duration=300):
    """Validate if the media duration is within the allowed limit (5 minutes = 300 seconds)."""
    duration = get_media_duration(file_path)
    if duration is not None:
        if duration > max_duration:
            logging.error(f"Media duration exceeds 5 minutes: {duration / 60:.2f} minutes")
            raise ValueError("Audio/video file is too long. Please limit to 5 minutes.")
        else:
            logging.info(f"Media duration is valid: {duration / 60:.2f} minutes")
    else:
        logging.error("Unable to validate media duration.")
        raise ValueError("Unable to determine the media duration.")