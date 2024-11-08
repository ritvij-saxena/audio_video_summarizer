#!/usr/bin/env python3

import logging
from custom_args_parser_error_handler import CustomArgumentParser

def main():
    logging.info("Starting Video/Audio to Text Summarizer")

    parser = CustomArgumentParser(description="Video/Audio to Text Summarizer CLI Tool")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-a", "--audio", type=str, help="Path to audio file to be summarized")
    group.add_argument("-p", "--playlist", type=str, help="URL of YouTube playlist to download and summarize")
    group.add_argument("-v", "--video", type=str, help="Path to video file to be summarized")

    args = parser.parse_args()

    if args.audio:
        logging.info("Audio file provided, beginning transcription and summarization.")
        logging.info("Path: " + args.audio)
        pass

    elif args.video:
        logging.info("Video file provided, converting to audio, then transcribing and summarizing.")
        pass

    elif args.playlist:
        logging.info("YouTube playlist provided, downloading and summarizing each audio.")
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
