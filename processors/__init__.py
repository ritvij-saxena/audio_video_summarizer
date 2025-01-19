import os
import logging
import subprocess
import sys
import shutil
import platform
import requests
import time

from processors.audio_processor import AudioProcessor
from processors.base_processor import BaseProcessor
from processors.processor_registry import ProcessorRegistry
from processors.video_processor import VideoProcessor
from processors.youtube_link_processor import YoutubeLinkProcessor
from utils.ffmpeg_helper import ensure_ffmpeg

sys.path.append(os.path.dirname(__file__))

OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"  # smallest model for this usecase

def _check_ollama_installed():
    """Check if Ollama is installed."""
    return shutil.which("ollama") is not None

def install_ollama():
    """Guide the user to install Ollama based on their OS."""
    logging.info("🔍 Checking for Ollama installation...")

    if _check_ollama_installed():
        logging.info("✅ Ollama is already installed!")
        return True

    logging.error("❌ Ollama is not installed.")

    os_type = platform.system()

    if os_type == "Darwin":  # macOS
        logging.info("\n➡️ Install Ollama using Homebrew:\n   brew install ollama")
    elif os_type == "Linux":
        logging.info("\n➡️ Install Ollama using the official script:\n   curl -fsSL https://ollama.com/install.sh | sh")
    elif os_type == "Windows":
        logging.info("\n➡️ Download and install Ollama from:\n   https://ollama.com/download")
    else:
        logging.info("\n⚠️ Unsupported OS. Please install Ollama manually from:\n   https://ollama.com")

    return False

def start_ollama():
    """Ensure Ollama service is running."""
    try:
        # Run Ollama serve in the background
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logging.info("🚀 Ollama server started successfully.")
        
        # Wait for Ollama to be ready
        for _ in range(10):
            try:
                response = requests.get("http://localhost:11434")
                if response.status_code == 200:
                    logging.info("✅ Ollama server is running.")
                    return
            except requests.exceptions.ConnectionError:
                time.sleep(2)

        logging.error("❌ Ollama server failed to start.")
        sys.exit(1)

    except Exception as e:
        logging.error(f"⚠️ Failed to start Ollama: {e}")
        sys.exit("🚨 Please install Ollama and try again.")

def ensure_ollama_model():
    """Ensure the smallest model is available."""
    try:
        models = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if OLLAMA_MODEL not in models.stdout:
            logging.info(f"📥 Downloading Ollama model: {OLLAMA_MODEL} ...")
            subprocess.run(["ollama", "pull", OLLAMA_MODEL], check=True)
            logging.info("✅ Model downloaded successfully!")
        else:
            logging.info(f"✅ Ollama model '{OLLAMA_MODEL}' is already installed.")
    except Exception as e:
        logging.error(f"❌ Failed to check or download model: {e}")
        sys.exit(1)

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

    # Check and start Ollama
    if not install_ollama():
        sys.exit("🚨 Ollama is required but not installed.")

    start_ollama()
    ensure_ollama_model()

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