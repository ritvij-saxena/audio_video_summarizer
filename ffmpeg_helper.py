#!/usr/bin/env python3

import logging
import subprocess
import os

# Paths
FFMPEG_PATH = "third-party/ffmpeg/ffmpeg"
FFMPEG_REPO_URL = "https://git.ffmpeg.org/ffmpeg.git"
FFMPEG_SOURCE_PATH = "third-party/ffmpeg"
DOWNLOAD_URL = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-i686-static.tar.xz"  # Example URL for precompiled binary


def check_ffmpeg():
    """Check if the FFmpeg binary exists and works."""
    logging.info("Checking if the FFmpeg binary exists and works.")
    if os.path.exists(FFMPEG_PATH):
        try:
            subprocess.run([FFMPEG_PATH, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            logging.error("FFmpeg binary is found but not working.")
            return False
    return False


def download_ffmpeg():
    """Download and extract the FFmpeg binary if it doesn't exist."""
    logging.info("FFmpeg binary not found. Downloading FFmpeg...")
    try:
        # Download the FFmpeg tarball (example: precompiled binary)
        subprocess.run(["curl", "-L", "-o", "ffmpeg-release.tar.xz", DOWNLOAD_URL], check=True)

        # Extract the tarball
        subprocess.run(["tar", "-xvf", "ffmpeg-release.tar.xz", "-C", "third-party/ffmpeg"], check=True)

        logging.info("FFmpeg binary downloaded and extracted successfully.")
        os.remove("ffmpeg-release.tar.xz")  # Clean up the tarball

    except subprocess.CalledProcessError as e:
        logging.error(f"Error downloading FFmpeg: {e}")
        return False

    return True


def build_ffmpeg():
    """Run ./configure and make to build FFmpeg from source."""
    logging.info("FFmpeg binary not found. Building from source...")
    try:
        # Step 1: Clone the FFmpeg repository if not already cloned
        if not os.path.exists(FFMPEG_SOURCE_PATH):
            subprocess.run(["git", "clone", FFMPEG_REPO_URL, FFMPEG_SOURCE_PATH], check=True)

        # Step 2: Change to the FFmpeg directory
        os.chdir(FFMPEG_SOURCE_PATH)

        # Step 3: Run ./configure
        logging.info("Running ./configure...")
        logging.info("It might take a while! Hang in there...")
        subprocess.run(["./configure"], check=True)

        # Step 4: Build FFmpeg using make
        logging.info("Building FFmpeg with make...")
        subprocess.run(["make"], check=True)

        # Ensure the binary has execute permissions
        subprocess.run(["chmod", "+x", FFMPEG_PATH], check=True)

        # Step 5: Check if ffmpeg works
        if not check_ffmpeg():
            logging.error("FFmpeg build completed, but the binary is not working.")
            return False

        logging.info("FFmpeg built successfully and is working.")
        os.chdir("../../")  # Go back to the original directory

    except subprocess.CalledProcessError as e:
        logging.error(f"Error during FFmpeg build process: {e}")
        return False

    return True
