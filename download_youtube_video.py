import yt_dlp as youtube_dl
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Default download path
DEFAULT_DOWNLOAD_PATH = './youtube_downloads'
FFMPEG_PATH = "third-party/ffmpeg/ffmpeg"

def download_video_from_youtube(youtube_url: str):
    try:
        # Create the download directory if it doesn't exist
        if not os.path.exists(DEFAULT_DOWNLOAD_PATH):
            os.makedirs(DEFAULT_DOWNLOAD_PATH)

        # Set up youtube-dl options
        ydl_opts = {
            'ffmpeg_location': FFMPEG_PATH,
            'format': 'bestvideo+bestaudio/best',  # Download best video and audio
            'outtmpl': os.path.join(DEFAULT_DOWNLOAD_PATH, '%(title)s.%(ext)s'),  # Save video with title as filename
            'noplaylist': True,  # Prevent downloading playlists
            'quiet': False,  # Show download progress
        }

        # Download video using youtube-dl
        logging.info("Downloading video using yt-dl")
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(youtube_url, download=True)
            if 'entries' in result:
                video_info = result['entries'][0]
            else:
                video_info = result

            # Return the path to the downloaded video file
            logging.info("Returning the path to the downloaded video file")
            downloaded_video_path = os.path.join(DEFAULT_DOWNLOAD_PATH, video_info['title'] + '.' + video_info['ext'])
            logging.info(f"Downloaded video to: {downloaded_video_path}")
            return downloaded_video_path

    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        raise