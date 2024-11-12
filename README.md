# Audio/Video Summarizer 

(WORK IN PROGRESS)

This project is a command-line tool that transcribes and summarizes audio and video files. It utilizes **whisper.cpp** for transcription, and **Hugging Face's BART** model for summarization.

## Features

- Transcribes audio files using **whisper.cpp**.
- Summarizes transcriptions with **BART** from Hugging Face.
- Supports both local audio files (`.wav` format) and video files.
- Option to download and summarize YouTube playlist audio (feature in progress).
- Automatically handles model download and compilation if needed.

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/ritvij-saxena/audio_video_summarizer.git
cd audio_video_summarizer
```

### 2. Set up a virtual environment (optional, but recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies:

Make sure you have the required libraries installed by using the `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Set up Whisper model and compile `whisper.cpp` (mandatory):

The tool will attempt to download the Whisper model and compile **whisper.cpp** automatically if not already set up. Ensure that you have internet access to download the necessary resources.

## Usage

### Command-line Arguments:

- `-a, --audio`: Path to the `.wav` audio file to be transcribed and summarized.
- `-v, --video`: Path to the video file to be converted to audio, transcribed, and summarized.
- `-p, --playlist`: URL of a YouTube playlist to download and summarize.

### Example Usage:

#### Summarize an Audio File:

```bash
python avs.py -a /path/to/audio.wav
```

This will transcribe the audio file and print the transcription along with a summary.

#### Summarize a Video File:

```bash
python avs.py -v /path/to/video.mp4
```

This will convert the video to audio, transcribe, and summarize the content.

#### Summarize a YouTube Playlist:

```bash
python avs.py -p "https://www.youtube.com/playlist?list=your_playlist_id"
```

This will download each video in the playlist, convert them to audio, transcribe, and summarize them.

## Code Overview

- **`avs.py`**: The main script that handles command-line interface (CLI) interaction, model downloading, compilation, and transcribing/summarizing the files.
- **`transcriber.py`**: Contains the function `transcribe_audio()` that handles audio transcription using **whisper.cpp**. It checks the file format, sample rate, and runs the transcription process.
- **`summarizer.py`**: Contains the function `summarize_transcription()` which summarizes the transcribed text using **Hugging Face's BART** model.
- **`custom_args_parser_error_handler.py`**: Custom argument parser for error handling during CLI interactions.

## Notes

- The tool currently supports `.wav` files for audio transcription.
- The sample rate for `.wav` files must be 16 kHz. If a file with a different sample rate is provided, it will be converted automatically using **ffmpeg**.
- The video and YouTube playlist features are in progress.

## Contributing

Feel free to fork this repository, open issues, or create pull requests if you'd like to contribute.

## License

This project is licensed under the MIT License.
