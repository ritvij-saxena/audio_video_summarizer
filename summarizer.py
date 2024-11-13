import logging
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration

def summarize_transcription(transcription_data):
    """Summarize the transcription data text."""
    if not transcription_data:
        logging.error(f"Argument \"transcription_data\" was {transcription_data}")
        return ""

    # Concatenate all text segments into a single text block
    full_text = " ".join([entry['text'] for entry in transcription_data])

    # Check for very long text and handle it
    max_input_length = 1024  # BART's typical max input length (tokens)
    if len(full_text.split()) > max_input_length:
        logging.warning(f"Input text length exceeds {max_input_length} tokens, truncating.")
        full_text = " ".join(full_text.split()[:max_input_length])  # Truncate to the model's max length

    # Initialize a summarization pipeline (using Hugging Face Transformers)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    # Perform summarization
    try:
        summary = summarizer(full_text, max_length=50, min_length=25, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Summarization failed: {e}")
        return ""
