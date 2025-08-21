import streamlit as st
import pyttsx3
import tempfile
import os
import speech_recognition as sr
from datetime import datetime
import streamlit as st
import qrcode
from io import BytesIO

# ========== UTILITIES ==========

def text_to_speech(text, voice_id):
    engine = pyttsx3.init()
    engine.setProperty('voice', voice_id)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        filename = tmp_file.name
    engine.save_to_file(text, filename)
    engine.runAndWait()
    with open(filename, "rb") as f:
        audio_bytes = f.read()
    os.remove(filename)
    return audio_bytes

def save_note(text):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"note_{timestamp}.txt"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(text)
    return filename

# ========== INDIVIDUAL PROJECTS ==========

def project_text_to_speech():
    st.header("🗣️ Text to Speech")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    male_voice = voices[0].id
    female_voice = voices[1].id

    user_text = st.text_area("Enter text to convert to speech:")
    voice_choice = st.selectbox("Select voice type:", ["Male", "Female"])

    if st.button("🔊 Create and Play"):
        if not user_text.strip():
            st.warning("Please enter some text.")
            return
        voice_id = male_voice if voice_choice == "Male" else female_voice
        audio_bytes = text_to_speech(user_text, voice_id)
        st.audio(audio_bytes, format="audio/wav")

def speech_to_text():
    st.header("🎙️ Speech to Text Note Saver")
    recognizer = sr.Recognizer()

    if st.button("🎤 Start Recording"):
        with sr.Microphone() as source:
            st.info("Listening... Speak now.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            st.success("Transcribing...")
            text = recognizer.recognize_google(audio)
            st.text_area("Transcribed Text:", value=text, height=150)

            if st.button("💾 Save Note"):
                filename = save_note(text)
                st.success(f"✅ Note saved as `{filename}`")

        except sr.UnknownValueError:
            st.error("❌ Could not understand your speech.")
        except sr.RequestError as e:
            st.error(f"🚫 Speech recognition service error: {e}")

def project_sentiment_analyzer():
    st.header("Sentiment Analyzer (Coming Soon)")
    st.info("This tool will analyze your text and tell if it's positive, negative, or neutral.")

def project_qr_code_generator():
    st.header("📱 QR Code Generator")
    st.write("Convert any text, URL, or message into a QR code.")

    user_input = st.text_input("Enter text or link to generate QR code:")

    if st.button("Generate QR Code"):
        if not user_input.strip():
            st.warning("⚠️ Please enter some text or a link.")
            return
        
        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )
        qr.add_data(user_input)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")

        # Convert image to BytesIO for Streamlit display
        buf = BytesIO()
        img.save(buf)
        buf.seek(0)

        # Display the image
        st.image(buf, caption="Your QR Code", use_column_width=False)
        st.success("✅ QR Code generated!")

def project_placeholder(name):
    st.header(f"{name}")
    st.info("This project is under construction.")

# ========== MAIN FUNCTION ==========

def main():
    st.set_page_config(page_title="Ahmad's Idea Vault", layout="wide")

    # Custom CSS for dark theme and styling
    st.markdown("""
        <style>
            .main-title {
                font-size: 48px;
                font-weight: 900;
                text-align: center;
                color: #F1F1F1;
                margin-top: 30px;
                margin-bottom: 10px;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .sub-caption {
                text-align: center;
                font-size: 18px;
                color: #BBBBBB;
                margin-bottom: 40px;
                font-style: italic;
            }
            .block-container {
                padding-top: 2rem;
                background-color: #121212;
            }
            .css-18e3th9 {
                background-color: #121212;
                color: white;
            }
            .stSelectbox label, .stTextArea label {
                color: #CCCCCC !important;
            }
            .stButton>button {
                background-color: #1F77B4;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 0.5rem 1rem;
                font-weight: bold;
            }
            .stAudio {
                background-color: #1e1e1e;
                border-radius: 8px;
                padding: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Custom title
    st.markdown('<div class="main-title">Ahmad\'s Idea Vault</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-caption">Explore and experiment with my creative projects</div>', unsafe_allow_html=True)

    # Sidebar menu
    project = st.sidebar.selectbox("Select a project:", [
        "Text to Speech",
        "Speech to Text",
        "Sentiment Analyzer",
        "QR Code Generator",
        "Project 4",
        "Project 5"
    ])

    # Routing
    if project == "Text to Speech":
        project_text_to_speech()
    elif project == "Speech to Text":
        speech_to_text()
    elif project == "Sentiment Analyzer":
        project_sentiment_analyzer()
    elif project == "QR Code Generator":
        project_qr_code_generator()
    else:
        project_placeholder(project)

# ========== START APP ==========

if __name__ == "__main__":
    main()
