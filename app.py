# app.py
import streamlit as st
from audio_utils import start_recording, stop_recording, is_recording
from transcriber import transcribe
from responder import tts_bytes, map_lang
import os
import time

st.set_page_config(page_title="Speech AI - Start/Stop + TTS", layout="centered")
st.title("🎤 Speech AI — Start/Stop Recording + TTS (Whisper offline, gTTS online)")

# session state
if "notes" not in st.session_state:
    st.session_state.notes = []               # list of strings: saved transcriptions
if "last_transcription" not in st.session_state:
    st.session_state.last_transcription = ""
if "last_lang" not in st.session_state:
    st.session_state.last_lang = None
if "status" not in st.session_state:
    st.session_state.status = "Idle"

status_placeholder = st.empty()
controls_col, notes_col = st.columns([1, 1])

with controls_col:
    st.markdown("### Controls")
    # Start button
    if st.button("▶️ Start Recording"):
        started = start_recording()
        if started:
            st.session_state.status = "🎙 Recording..."
        else:
            st.session_state.status = "⚠️ Already recording"

    # Stop button
    if st.button("⏹ Stop & Transcribe"):
        if is_recording():
            st.session_state.status = "✅ Recording finished. 🔍 Transcribing..."
            status_placeholder.info(st.session_state.status)
            # stop recording and get file
            audio_path = stop_recording()
            if audio_path:
                # transcribe (blocking, may take time on CPU)
                try:
                    result = transcribe(audio_path)
                    text = result.get("text", "").strip()
                    lang = result.get("language", None)
                    st.session_state.last_transcription = text
                    st.session_state.last_lang = lang
                    # append note with language tag
                    tag = lang.upper() if lang else "UNK"
                    st.session_state.notes.append(f"[{tag}] {text}")
                    st.session_state.status = f"📝 Transcribed ({tag})"
                except Exception as e:
                    st.session_state.status = f"❌ Transcription error: {e}"
                finally:
                    # remove temp file
                    try:
                        os.remove(audio_path)
                    except OSError:
                        pass
            else:
                st.session_state.status = "⚠️ No audio captured"
        else:
            st.session_state.status = "⚠️ Not currently recording"

    # Speak button
    if st.button("🔊 Speak Last Transcription"):
        txt = st.session_state.last_transcription
        if not txt:
            st.warning("No transcription available to speak.")
        else:
            # map to gTTS code and get bytes, then show via st.audio
            lang_code = map_lang(st.session_state.last_lang)
            st.session_state.status = "🔊 Generating TTS..."
            status_placeholder.info(st.session_state.status)
            try:
                audio_bytes = tts_bytes(txt, lang_code)
                if audio_bytes:
                    st.session_state.status = "🔊 Playing..."
                    # show audio widget (plays in browser)
                    st.audio(audio_bytes, format="audio/mp3")
                else:
                    st.session_state.status = "❌ TTS returned no audio"
            except Exception as e:
                st.session_state.status = f"❌ TTS error: {e}"

    # clear notes
    if st.button("🗑 Clear Notes"):
        st.session_state.notes = []
        st.session_state.last_transcription = ""
        st.session_state.last_lang = None
        st.session_state.status = "Notes cleared"

# Status area (always visible)
status_placeholder.info(st.session_state.status)

with notes_col:
    st.subheader("📝 Notes (latest on top)")
    if st.session_state.notes:
        # show latest first
        for n in reversed(st.session_state.notes):
            st.write(n)
    else:
        st.write("_No notes yet_")

st.markdown("---")
st.caption("Recording uses your microphone. Transcription runs locally with Whisper; TTS uses online gTTS.")
