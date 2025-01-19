#!/usr/bin/env python3

import logging

from custom_args_parser_error_handler import CustomArgumentParser
from processors import process_input
from argument_groups import load_argument_groups

def setup_logging():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    setup_logging()
    logging.info("Starting Video/Audio to Text Summarizer")

    parser = CustomArgumentParser(description="Video/Audio to Text Summarizer CLI Tool. Extracts text from video/audio and summarizes it. \n\n \n Important Validation Rule:\n" \
                                              " - The video or audio file must not exceed 5 minutes in length. Files longer than this will not be processed.")
    load_argument_groups(parser)
    args = parser.parse_args()
    process_input(args)

if __name__ == "__main__":
    main()
