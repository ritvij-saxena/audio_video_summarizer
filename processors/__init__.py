import os
import importlib
import logging
import subprocess
import sys

from processors.audio_processor import AudioProcessor
from processors.base_processor import BaseProcessor
from processors.video_processor import VideoProcessor
from processors.youtube_link_processor import YoutubeLinkProcessor
from utils.ffmpeg_helper import ensure_ffmpeg

sys.path.append(os.path.dirname(__file__))

def download_whisper_model():
    try:
        logging.info("Downloading Whisper model...")
        subprocess.run(["sh", "./third-party/whisper.cpp/models/download-ggml-model.sh", "base.en"], check=True)
    except subprocess.CalledProcessError:
        logging.error("Failed to download the model. Check the download script.")
        return False
    return True

def build_whisper_cpp():
    try:
        logging.info("Building whisper.cpp...")
        subprocess.run(["make", "-j"], cwd="./third-party/whisper.cpp", check=True)
    except subprocess.CalledProcessError:
        logging.error("Failed to build whisper.cpp. Please check for any critical build errors.")
        return False
    return True

def process_input(args):
    """Dynamically processes input based on arguments."""
    if any(value is not None for value in vars(args).values()):

        if not download_whisper_model():
            logging.error("Download whisper failed. Please check the logs.")
            return

        if not build_whisper_cpp():
            logging.error("Build whisper failed. Please check the logs.")
            return

        if not ensure_ffmpeg():
            logging.error("ffmpeg setup failed. Please check the logs.")
            return

        # Ensure the processors directory exists and contains the modules
        current_dir = os.path.dirname(__file__)
        print(f"Current directory: {current_dir}")

        if not os.path.isdir(current_dir):
            logging.error(f"Processors directory does not exist: {current_dir}")
            return

        processor = None
        if args.audio:
            processor = AudioProcessor(args.audio)

        elif args.video:
            processor = VideoProcessor(args.video)

        elif args.youtube_link:
            processor = YoutubeLinkProcessor(args.youtube_link)

        processor.process()
    else:
        raise ValueError("No arguments provided.")
