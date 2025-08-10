# transcriber.py
from transformers import pipeline
import os

# load Whisper ASR pipeline once (CPU)
print("⏳ Loading Whisper ASR pipeline (openai/whisper-small)... this may take a minute on CPU")
_asr = pipeline("automatic-speech-recognition", model="openai/whisper-small", device=-1)
print("✅ Whisper ASR loaded.")

def transcribe(filepath, language=None, task="transcribe"):
    """
    Transcribe an audio file with Hugging Face Whisper pipeline.
    Returns a dict: { "text": ..., "language": <code or None> }
    - language param can be used to force language (e.g., "urdu" or "en"), but if None it auto-detects.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)

    # pipeline accepts filename directly
    # if you want to force language/transcribe vs translate, use generate_kwargs or kwargs here
    kwargs = {}
    if language:
        # whisper pipeline accepts generate_kwargs {"forced_decoder_ids": ...} is deprecated;
        # Instead pass "language" or "task" newer flags are supported by HF pipeline
        kwargs["generate_kwargs"] = {"language": language, "task": task}

    result = _asr(filepath, **kwargs)
    text = result.get("text", "").strip()
    lang = result.get("language", None)  # HF returns language code in many versions
    return {"text": text, "language": lang}
