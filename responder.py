# responder.py
from gtts import gTTS
import tempfile
import os
import io

def tts_bytes(text, lang_code="en"):
    """
    Generate mp3 bytes for given text using gTTS (online).
    Returns bytes object containing MP3 data.
    """
    if not text:
        return None
    # gTTS expects some language codes like 'en', 'ur', etc.
    tts = gTTS(text=text, lang=lang_code)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tmp_name = tmp.name
    tmp.close()
    tts.save(tmp_name)
    # read bytes
    with open(tmp_name, "rb") as f:
        data = f.read()
    try:
        os.remove(tmp_name)
    except OSError:
        pass
    return data

# optional convenience: map whisper language codes/strings to gTTS codes
_lang_map = {
    "ur": "ur",
    "english": "en",
    "en": "en",
    # add more as needed
}

def map_lang(hf_lang):
    """Convert HF language output to gTTS code (best-effort)."""
    if not hf_lang:
        return "en"
    l = str(hf_lang).lower()
    if l.startswith("ur"):
        return "ur"
    if l.startswith("en"):
        return "en"
    # try simple mapping
    return _lang_map.get(l, "en")
