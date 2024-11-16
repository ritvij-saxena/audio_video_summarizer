def register_arguments(parser):
    """Register arguments for YouTube summarization."""
    group = parser.add_argument_group("YouTube Arguments")
    group.add_argument(
        "-yl", "--youtube-link",
        type=str,
        help="URL of YouTube video to download and summarize"
    )
