import wave
import re
from piper import PiperVoice
from model_manager import ModelManager as Model
from playsound import playsound
voice = PiperVoice.load(Model().get_model_piper())


def clean_text_for_speech(text: str) -> str:
    """Clean text for better speech synthesis"""
    # Remove markdown formatting
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # **bold** -> bold
    text = re.sub(r'\*(.*?)\*', r'\1', text)      # *italic* -> italic
    text = re.sub(r'`(.*?)`', r'\1', text)        # `code` -> code
    text = re.sub(r'#{1,6}\s*', '', text)         # Remove # headers
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)  # [text](link) -> text

    # Remove special characters that sound bad
    text = re.sub(r'[•◦▪▫]', '', text)            # Remove bullet points
    text = re.sub(r'[-]{2,}', '', text)           # Remove multiple dashes
    text = re.sub(r'[=]{2,}', '', text)           # Remove equals signs
    text = re.sub(r'[\$]', 'dollars', text)       # $ -> dollars
    text = re.sub(r'[%]', 'percent', text)        # % -> percent
    text = re.sub(r'[&]', 'and', text)            # & -> and

    # Clean up mathematical expressions
    text = re.sub(r'\$\$.*?\$\$', 'mathematical expression', text)  # $$...$$
    text = re.sub(r'\$.*?\$', 'math', text)       # $...$

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()

    # Limit length to avoid very long speech
    if len(text) > 1800:
        text = text[:1797] + "..."

    return text


def speak_text(text: str):
    """Convert text to speech and play it.

    Args:
        text: The text to be spoken
    """
    text = clean_text_for_speech(text)
    with wave.open("output.wav", "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)
    playsound("output.wav")