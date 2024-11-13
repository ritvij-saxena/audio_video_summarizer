#!/usr/bin/env python3

import logging
import subprocess
from custom_args_parser_error_handler import CustomArgumentParser
from transcriber import transcribe_audio
from summarizer import summarize_transcription
from ffmpeg_helper import ensure_ffmpeg
from audio_extractor import extract_audio

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Video/Audio to Text Summarizer")

    # Download the Whisper model if it's not already present
    try:
        logging.info("Downloading Whisper model...")
        subprocess.run(["sh", "./third-party/whisper.cpp/models/download-ggml-model.sh", "base.en"], check=True)
    except subprocess.CalledProcessError:
        logging.error("Failed to download the model. Check the download script.")
        return

    # Build whisper.cpp if needed
    try:
        logging.info("Building whisper.cpp...")
        subprocess.run(["make", "-j"], cwd="./third-party/whisper.cpp", check=True)
    except subprocess.CalledProcessError:
        logging.error("Failed to build whisper.cpp. Please check for any critical build errors.")
        return

    # Check if ffmpeg exists or build/download it
    if not ensure_ffmpeg():
        logging.error("FFmpeg setup failed. Please check the logs.")
        return

    parser = CustomArgumentParser(description="Video/Audio to Text Summarizer CLI Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--audio", type=str, help="Path to audio file to be summarized")
    group.add_argument("-p", "--playlist", type=str, help="URL of YouTube playlist to download and summarize")
    group.add_argument("-v", "--video", type=str, help="Path to video file to be summarized")

    args = parser.parse_args()

    if args.audio:
        logging.info("Audio file provided, beginning transcription and summarization.")
        logging.info("Path: " + args.audio)
        transcript = transcribe_audio(args.audio) # returns list of [{"timestamp": timestamp, "text": text}]
        if transcript:
            logging.info("Transcription:")
            logging.info(transcript)
        summary = summarize_transcription(transcription_data=transcript)
        logging.info("Summary of the Text from the Audio:")
        logging.info(summary)

    elif args.video:
        logging.info("Video file provided, converting to audio, then transcribing and summarizing.")
        logging.info("Path: " + args.video)
        audio_path = extract_audio(args.video)
        transcript = transcribe_audio(audio_path) # returns list of [{"timestamp": timestamp, "text": text}]
        if transcript:
            logging.info("Transcription:")
            logging.info(transcript)
        summary = summarize_transcription(transcription_data=transcript)
        logging.info("Summary of the Text from the Audio:")
        logging.info(summary)

    elif args.playlist:
        logging.info("YouTube playlist provided, downloading and summarizing each audio.")
        logging.info("Path: " + args.playlist)
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
