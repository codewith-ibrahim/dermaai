
import os
from pathlib import Path

from dotenv import load_dotenv
from deepgram import DeepgramClient


# 1. Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# 2. Text-to-speech function
def text_to_speech(text: str) -> Path:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    # Get Deepgram API key
    api_key = os.getenv("DEEPGRAM_API_KEY")

    if not api_key:
        raise ValueError(
            "DEEPGRAM_API_KEY missing. Check your .env file."
        )

    # Initialize Deepgram client
    client = DeepgramClient(api_key=api_key)

    # Output audio file path
    audio_path = BASE_DIR / "doctor_response.mp3"

    # Generate speech
    audio = client.speak.v1.audio.generate(
        text=text,
        model="aura-2-thalia-en",
        encoding="mp3",
    )

    # Save generated audio
    with audio_path.open("wb") as file:
        for chunk in audio:
            file.write(chunk)

    print(f"Audio saved: {audio_path}")

    return audio_path


# 3. Test the function
if __name__ == "__main__":
    sample_text = (
        "Hello, I am DermaAI. "
        "How can I help you with your skin concerns today?"
    )

    audio_file = text_to_speech(sample_text)

    print(f"Generated audio file: {audio_file}")
