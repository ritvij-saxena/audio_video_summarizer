# Video/Audio to Text Summarizer CLI Tool

## Overview
The **Video/Audio to Text Summarizer** is a command-line tool that extracts text from video or audio files, transcribes the speech, and summarizes the content. It supports multiple input formats, including direct audio files, video files, and YouTube video links. 
**This tool can process content up to 5 minutes in length only.** (Future improvements)

## Features
- **Transcription**: Extracts speech from audio/video files and provides timestamps for each segment.
- **Summarization**: Summarizes the transcribed content to generate a concise summary.
- **Supports Multiple Input Formats**: Works with audio files, video files, and YouTube video links.
- **Automatic Video to Audio Conversion**: If a video file is provided, it will be converted to audio automatically before transcription.
- **Customizable Workflow**: Easy integration into your pipeline for audio/video transcription and summarization.

## Requirements

- **Python 3.9+**: Make sure you have Python 3.9 or later installed.
- **FFmpeg**: FFmpeg must be available in your system for video/audio processing.
- **Whisper.cpp**: A C++ implementation of the Whisper model for transcription. The tool will download and build this model automatically.

## Installation

### Clone the Repository

```bash
git clone https://github.com/your-repository/audio-video-summarizer.git
cd audio-video-summarizer
```

### Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Setup
1. **Download and Build Whisper.cpp**: The tool will automatically download and build the Whisper model when first executed.

2. **FFmpeg Setup**: The tool checks for the availability of FFmpeg. If it's not installed, follow the instructions to install it.

## Usage

### Command-Line Arguments

The tool accepts three types of inputs:
- **Audio File (`-a` or `--audio`)**: Provides the path to an audio file for transcription and summarization.
- **Video File (`-v` or `--video`)**: Provides the path to a video file, which will be converted to audio before transcription and summarization.
- **YouTube Link (`-yl` or `--youtube-link`)**: Provides a YouTube URL. The video is downloaded, converted to audio, and processed.

### Example Commands

#### 1. Process Audio File

```bash
./avs -a /path/to/audio/file.wav
```

#### 2. Process Video File

```bash
./avs -v /path/to/video/file.mp4
```

#### 3. Process YouTube Video

```bash
./avs -yl "https://www.youtube.com/watch?v=example"
```

### Important Validation Rule
- The video or audio file must **not exceed 5 minutes in length**. Files longer than this will not be processed.
- Only `.wav` audio files are allowed.
- Only `".mp4", ".avi", ".mov", ".mkv", ".flv", ".webm"` video files are allowed.

## Architecture

1. **Model Download**: The first time the tool runs, it downloads the Whisper model automatically using the script located at `./third-party/whisper.cpp/models/download-ggml-model.sh`.
2. **Video/Audio Processing**: FFmpeg is used to extract audio from video files. Audio files are transcribed using Whisper.cpp, and the resulting text is summarized.

## Dependencies

- `python-youtube-dl`: For downloading YouTube videos.
- `ffmpeg`: For processing video/audio files.
- `whisper.cpp`: For speech-to-text transcription.

### Helper Scripts
- **CustomArgumentParser**: Custom argument parser with error handling.
- **Transcriber**: Transcribes audio content using Whisper.cpp.
- **Summarizer**: Summarizes the transcribed content.
- **FFmpeg Helper**: Ensures FFmpeg is available and configured.
- **Audio Extractor**: Converts video files to audio.
- **YouTube Downloader**: Downloads YouTube videos and returns the video file path.

## Troubleshooting

- **FFmpeg Setup**: If the tool fails to find FFmpeg, ensure that FFmpeg is installed on your system and available in the PATH.
- **Whisper Model Download**: If the model download fails, check the logs for errors related to the download script or internet connectivity.
- **Video to Audio Conversion**: If video to audio conversion fails, ensure that the video file is in a supported format and that FFmpeg is working correctly.

**NOTE**: If any of the tools (FFmpeg, Whisper.cpp, ffmpeg-python) encounter issues, please verify that their corresponding binaries are downloaded and placed in the appropriate directory under `/third-party`.

## Contributing

We welcome contributions to improve the tool. To contribute:
1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a description of your changes.


## Contact

For any questions or issues, please feel free to open an issue.

### Key Features:
1. **Setup**: It covers setting up the virtual environment, installing dependencies, and ensuring required tools (like FFmpeg and Whisper.cpp binaries) are present.
2. **Command-line usage**: Three key use cases for processing audio, video, and YouTube links are shown.
3. **Architecture and Dependencies**: Describes the components involved in the tool’s pipeline.
4. **Troubleshooting**: Helpful tips for common issues with FFmpeg, Whisper model download, and audio extraction.