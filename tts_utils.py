import uuid
from gtts import gTTS

def tts_output(text: str) -> str:
    """Convert text to speech and save as mp3."""
    filename = f"audio_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename