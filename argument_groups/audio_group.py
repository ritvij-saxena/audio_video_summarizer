def register_arguments(parser):
    """Register arguments for audio summarization."""
    group = parser.add_argument_group("Audio Arguments")
    group.add_argument(
        "-a", "--audio",
        type=str,
        help="Path to audio file to be summarized"
    )
