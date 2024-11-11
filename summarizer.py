from transformers import pipeline

def summarize_transcription(transcription_data):
    """Summarize the transcription data text."""

    # Concatenate all text segments into a single text block
    full_text = " ".join([entry['text'] for entry in transcription_data])

    # Initialize a summarization pipeline (using Hugging Face Transformers)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Perform summarization
    summary = summarizer(full_text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']