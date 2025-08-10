# audio_utils.py
import sounddevice as sd
import numpy as np
import soundfile as sf
import tempfile
import threading
import time
import os

# Recording config
_SAMPLE_RATE = 16000
_CHANNELS = 1

_recording_lock = threading.Lock()
_frames = []
_stream = None
_is_recording = False

def _callback(indata, frames_count, time_info, status):
    """sounddevice callback: append incoming audio frames to _frames"""
    if status:
        # status may contain warnings (e.g. overflow)
        # we don't raise here; Streamlit will show status updates
        pass
    with _recording_lock:
        _frames.append(indata.copy())

def start_recording(sample_rate=_SAMPLE_RATE, channels=_CHANNELS):
    """Start background recording (non-blocking)."""
    global _stream, _frames, _is_recording
    if _is_recording:
        return False  # already recording

    _frames = []
    _is_recording = True

    # Use InputStream with the callback; run it in a thread so Streamlit doesn't block
    def _run_stream():
        global _stream, _is_recording
        try:
            with sd.InputStream(samplerate=sample_rate, channels=channels, callback=_callback):
                # keep stream alive until stop_recording sets _is_recording False
                while _is_recording:
                    time.sleep(0.1)
        except Exception as e:
            # stream error will be handled by caller UI via return value / exceptions
            _is_recording = False
            raise

    t = threading.Thread(target=_run_stream, daemon=True)
    t.start()
    return True

def stop_recording(filename=None):
    """Stop recording and write to a WAV file. Returns file path or None."""
    global _is_recording, _frames
    if not _is_recording:
        return None
    _is_recording = False

    # Wait a moment to ensure all frames flushed
    time.sleep(0.2)

    # Concatenate frames
    with _recording_lock:
        if len(_frames) == 0:
            return None
        data = np.concatenate(_frames, axis=0)

    # Ensure dtype is float32 for soundfile, normalize if needed
    # sounddevice default dtype is float32 or int16 depending on platform - cover both
    if np.issubdtype(data.dtype, np.integer):
        # convert int16 -> float32 [-1,1]
        max_val = np.iinfo(data.dtype).max
        data = data.astype('float32') / max_val
    else:
        data = data.astype('float32')

    if filename is None:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        filename = tmp.name
        tmp.close()

    # Write WAV with soundfile
    sf.write(filename, data, _SAMPLE_RATE, format='WAV')
    return filename

def is_recording():
    return _is_recording
