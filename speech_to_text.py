
import os
import logging
from pathlib import Path
from io import BytesIO

import speech_recognition as sr
from pydub import AudioSegment
from dotenv import load_dotenv
from groq import Groq


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)


def speech_to_text(
    audio_filepath: str | None = None,
    timeout: int = 20,
    phrase_time_limit: int = 10,
) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY missing in .env")

    # If no audio file is supplied, record from microphone.
    if not audio_filepath:
        recognizer = sr.Recognizer()

        try:
            with sr.Microphone() as source:
                logging.info("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(
                    source, duration=1
                )

                logging.info("Start speaking...")
                audio_data = recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit,
                )

            wav_data = audio_data.get_wav_data()
            segment = AudioSegment.from_wav(BytesIO(wav_data))

            audio_path = BASE_DIR / "recorded_audio.mp3"
            segment.export(audio_path, format="mp3", bitrate="128k")
            audio_filepath = str(audio_path)

        except sr.WaitTimeoutError:
            logging.warning("No speech detected.")
            return ""
        except OSError as error:
            raise RuntimeError(
                "Microphone unavailable. Check microphone permissions."
            ) from error

    audio_path = Path(audio_filepath).expanduser().resolve()

    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    client = Groq(api_key=api_key)

    try:
        with audio_path.open("rb") as audio_file:
            result = client.audio.transcriptions.create(
                file=audio_file,
                model=os.getenv("WHISPER_MODEL", "whisper-large-v3"),
            )

        text = (result.text or "").strip()

        if not text:
            logging.warning("No speech could be transcribed.")
            return ""

        logging.info("Speech transcribed successfully.")
        return text

    except Exception as error:
        raise RuntimeError(
            f"Groq transcription failed: {error}"
        ) from error


if __name__ == "__main__":
    transcript = speech_to_text()
    print("Transcript:", transcript)
