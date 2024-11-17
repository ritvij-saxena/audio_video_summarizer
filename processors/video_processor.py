from processors.base_processor import BaseProcessor
from utils.audio_extractor import extract_audio
from utils.summarizer import summarize_transcription
from utils.transcriber import transcribe_audio


class VideoProcessor(BaseProcessor):
    def __init__(self, video_path):
        self.video_path = video_path

    def process(self):
        video_path = self.video_path
        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
        summary = summarize_transcription(transcript)
        print(summary)