#!/usr/bin/env python3

import logging
import subprocess

from custom_args_parser_error_handler import CustomArgumentParser
from transcriber import transcribe_audio
from summarizer import summarize_transcription
from ffmpeg_helper import ensure_ffmpeg
from audio_extractor import extract_audio
from download_youtube_video import download_video_from_youtube

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

def process_audio_file(audio_path):
    logging.info("Audio file provided, beginning transcription and summarization.")
    transcript = transcribe_audio(audio_path)  # returns list of [{"timestamp": timestamp, "text": text}]
    if transcript:
        logging.info("Transcription:")
        logging.info(transcript)
    summary = summarize_transcription(transcription_data=transcript)
    logging.info("Summary of the Text from the Audio:")
    logging.info(summary)

def process_video_file(video_path):
    logging.info("Video file provided, converting to audio, then transcribing and summarizing.")
    audio_path = extract_audio(video_path)
    if not audio_path:
        logging.error("Video to audio conversion failed...")
        return
    process_audio_file(audio_path)

def process_youtube_link(youtube_link):
    logging.info("YouTube link provided, downloading and summarizing audio.")
    video_path = download_video_from_youtube(youtube_link)
    audio_path = extract_audio(video_path)
    if not audio_path:
        logging.error("Video to audio conversion failed...")
        return
    process_audio_file(audio_path)

def main():
    setup_logging()
    logging.info("Starting Video/Audio to Text Summarizer")

    parser = CustomArgumentParser(description="Video/Audio to Text Summarizer CLI Tool. Extracts text from video/audio and summarizes it. \n\n \n Important Validation Rule:\n" \
                                              " - The video or audio file must not exceed 5 minutes in length. Files longer than this will not be processed.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--audio", type=str, help="Path to audio file to be summarized")
    group.add_argument("-yl", "--youtube-link", type=str, help="URL of YouTube video to download and summarize")
    group.add_argument("-v", "--video", type=str, help="Path to video file to be summarized")
    args = parser.parse_args()

    if len(vars(args)) > 1:
        if not download_whisper_model():
            return
        if not build_whisper_cpp():
            return

        # Check if ffmpeg exists or build/download it
        if not ensure_ffmpeg():
            logging.error("FFmpeg setup failed. Please check the logs.")
            return

        if args.audio:
            process_audio_file(args.audio)

        elif args.video:
            process_video_file(args.video)

        elif args.youtube_link:
            process_youtube_link(args.youtube_link)


if __name__ == "__main__":
    main()
