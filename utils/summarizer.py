import logging
from transformers import pipeline, BartTokenizer, BartForConditionalGeneration

def summarize_transcription(transcription_data):
    """Summarize the transcription data text into a concise, meaningful summary."""
    if not transcription_data:
        logging.error(f"Argument \"transcription_data\" was {transcription_data}")
        return ""

    # Concatenate all text segments into a single text block
    full_text = " ".join([entry['text'] for entry in transcription_data])

    # Initialize the tokenizer and model (for tokenization and chunking)
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

    # Maximum token length for BART
    max_input_length = 1024  # Maximum number of tokens BART can handle

    # Split the full text into smaller chunks if it's too large
    def split_into_chunks(text, max_length):
        # Tokenize the text and split into chunks
        tokens = tokenizer.encode(text)
        chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
        return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]

    chunks = split_into_chunks(full_text, max_input_length)

    # Initialize a summarization pipeline
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

    # Summarize each chunk separately
    summaries = []
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=200, min_length=75, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            logging.error(f"Error summarizing chunk: {e}")
            continue

    # Combine the chunk summaries into a single text block
    combined_summary = " ".join(summaries)

    # Summarize the combined summaries (for refinement)
    try:
        final_summary = summarizer(combined_summary, max_length=200, min_length=75, do_sample=False)
        return final_summary[0]['summary_text']
    except Exception as e:
        logging.error(f"Error summarizing combined summary: {e}")
        return "Error during final summarization."

