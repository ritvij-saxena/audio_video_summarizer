def register_arguments(parser):
    """Register arguments for video summarization."""
    group = parser.add_argument_group("Video Arguments")
    group.add_argument(
        "-v", "--video",
        type=str,
        help="Path to video file to be summarized"
    )
