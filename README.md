# 🎙️ Speech_Ai: Real-Time Speech Recorder and Text-to-Speech with Streamlit

Speech_Ai is an interactive Streamlit application that allows you to record audio from your microphone, transcribe it to text using Google’s speech recognition, and convert the transcription back to speech with offline text-to-speech (TTS). It’s designed for flexible, unlimited recording sessions with easy start/stop controls and a simple UI.

## 🚀 Features
- 🎤 Start and stop recording from microphone without fixed time limits  
- 📝 Real-time transcription using Google Speech Recognition API  
- 🔊 Text-to-Speech playback of the transcribed text with pyttsx3  
- 🖥️ Simple, clean Streamlit UI with intuitive buttons  
- 🔄 Local offline TTS engine (no API required)  
- 🎛️ No sliders or recording time restrictions—manual control only  

## 🧰 Tech Stack
| Component           | Description                                 |
|---------------------|---------------------------------------------|
| 🎙️ Streamlit        | Web-based frontend UI                        |
| 🔗 streamlit-webrtc  | Real-time audio streaming and capture       |
| 🗣️ SpeechRecognition| Speech-to-text using Google Web Speech API  |
| 🔊 pyttsx3           | Offline text-to-speech engine                 |
| 🐍 Python           | Core language and environment                |

## 🔧 Running the App
1. Install dependencies:
    ```bash
    pip install streamlit streamlit-webrtc speechrecognition pyttsx3 pyaudio
    ```
2. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3. Use the buttons to start recording, stop recording, and play TTS.

## 📦 Requirements
- Python 3.7 or higher  
- Microphone access enabled in your browser  

## 🧑‍💻 Author
**Saad Saddique**  
AI/ML Developer | Speech & NLP Enthusiast

## 📜 License
MIT License
