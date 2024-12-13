from processors.base_processor import BaseProcessor
from utils.transcriber import transcribe_audio
from utils.summarizer import summarize_transcription

class AudioProcessor(BaseProcessor):
    def process(self):
        audio_path = self.path
        transcript = transcribe_audio(audio_path)
        summary = summarize_transcription(transcript)
        self.print_summary(summary)
