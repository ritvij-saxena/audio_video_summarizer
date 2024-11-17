from processors.base_processor import BaseProcessor
from utils.transcriber import transcribe_audio
from utils.summarizer import summarize_transcription

class AudioProcessor(BaseProcessor):
    def __init__(self, audio_path):
        self.audio_path = audio_path

    # def can_process(self, args):
    #     return args.audio is not None

    def process(self):
        audio_path = self.audio_path
        transcript = transcribe_audio(audio_path)
        summary = summarize_transcription(transcript)
        print(summary)
