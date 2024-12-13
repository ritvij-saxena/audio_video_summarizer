import os
import logging
import subprocess
import sys

from processors.audio_processor import AudioProcessor
from processors.base_processor import BaseProcessor
from processors.processor_registry import ProcessorRegistry
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

def ensure_dependencies():
    """Ensure all required dependencies are installed and working."""
    logging.info("Checking FFMPEG binary is present")
    if not ensure_ffmpeg():
        raise RuntimeError("FFmpeg is not installed or not working. Please resolve the issue.")

    logging.info("Checking whisper.cpp binary is present else download it")
    if not download_whisper_model():
        raise RuntimeError("Failed to download Whisper model.")

    logging.info("Building whisper.cpp binary is present else download it")
    if not build_whisper_cpp():
        raise RuntimeError("Failed to build whisper.cpp. Please resolve build issues.")

def process_input(args):
    """Dynamically processes input based on arguments."""
    ensure_dependencies()

    if not any(value is not None for value in vars(args).values()):
        raise ValueError("No arguments provided.")

    # Discover processors dynamically
    processors_dir = os.path.dirname(__file__)
    ProcessorRegistry.discover_processors(processors_dir)


    # Process the input based on the provided arguments
    for arg, value in vars(args).items():
        if value is not None:
            processor_class = ProcessorRegistry.get_processor(arg)
            if processor_class:
                processor_instance = processor_class(value)
                processor_instance.process()
                return
            else:
                logging.error(f"No processor registered for {arg}")

    raise ValueError("No suitable processor found for the provided input.")