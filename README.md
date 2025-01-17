# Video/Audio to Text Summarizer CLI Tool

## Overview

The **Video/Audio to Text Summarizer** is a command-line tool that extracts text from video or audio files, transcribes the speech, and summarizes the content. It supports multiple input formats, including direct audio files, video files, and YouTube video links.
**This tool can process content up to 5 minutes in length only.** (Future improvements)

## Features

- **Transcription**: Extracts speech from audio/video files and provides timestamps for each segment.
- **Summarization**: Summarizes the transcribed content to generate a concise summary.
- **Supports Multiple Input Formats**: Works with audio files, video files, and YouTube video links.
- **Automatic Video to Audio Conversion**: If a video file is provided, it will be converted to audio automatically before transcription.
- **Cross-Platform Executables**: Prebuilt binaries available for Windows, macOS, and Linux.

## Installation & Setup

### Option 1: Download Prebuilt Executable (Recommended)

#### **For Windows, macOS, and Linux**

1. Download the latest executable from the [Releases](https://github.com/your-repository/audio-video-summarizer/releases).
2. Extract the file and navigate to the extracted folder.
3. Run the executable using:

```sh
# On Linux/macOS
chmod +x avs
./avs -yl "https://www.youtube.com/watch?v=example"

# On Windows (Run in PowerShell or CMD)
avs.exe -yl "https://www.youtube.com/watch?v=example"
```

### Option 2: Run from Source (Requires Python & Dependencies)

#### **Clone the Repository**

```bash
git clone https://github.com/your-repository/audio-video-summarizer.git
cd audio-video-summarizer
```

#### **Set Up Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### **Install Dependencies**

```bash
pip install -r requirements.txt
```

## Usage

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

## Cross-Platform Build Setup

We use **GitHub Actions** to generate executables for **Windows, macOS, and Linux** automatically.

### **Building the Executable Locally**

To generate a single-file executable on your machine:

```sh
pip install pyinstaller
pyinstaller --onefile --name avs avs
```

- The binary will be in the `dist/` directory.

### **Automated GitHub Action Build**

GitHub automatically builds executables for all platforms on each push.

#### **How to Create a New Release**

1. Push changes to GitHub.
2. Navigate to **GitHub Releases**.
3. Download the appropriate binary for your platform.

## Troubleshooting

- **FFmpeg Setup**: If the tool fails to find FFmpeg, ensure that FFmpeg is installed on your system and available in the PATH.
- **Whisper Model Download**: If the model download fails, check the logs for errors related to the download script or internet connectivity.
- **Video to Audio Conversion**: If video to audio conversion fails, ensure that the video file is in a supported format and that FFmpeg is working correctly.

## Contributing

We welcome contributions to improve the tool. To contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a description of your changes.

## Contact

For any questions or issues, please feel free to open an issue.
