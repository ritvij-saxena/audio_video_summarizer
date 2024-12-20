from utils.audio_extractor import extract_audio
from processors.base_processor import BaseProcessor
from utils.download_youtube_video import download_video_from_youtube
from utils.summarizer import summarize_transcription
from utils.transcriber import transcribe_audio


class YoutubeLinkProcessor(BaseProcessor):
    def process(self):
        youtube_link = self.path
        video_path = download_video_from_youtube(youtube_link)
        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
        summary = summarize_transcription(transcript)
        self.print_summary(summary)
