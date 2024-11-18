from processors.base_processor import BaseProcessor
from utils.audio_extractor import extract_audio
from utils.summarizer import summarize_transcription
from utils.transcriber import transcribe_audio


class VideoProcessor(BaseProcessor):
    def process(self):
        video_path = self.path
        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
        summary = summarize_transcription(transcript)
        print(summary)