
import os
import time
import mimetypes
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types


# 1. Load environment variables
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


# 2. Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY missing. Check your .env file."
    )

client = genai.Client(api_key=api_key)

MODEL = "gemini-robotics-er-2-preview"


# 3. Read file content
def encode_file(filepath: str) -> bytes:
    with open(filepath, "rb") as file:
        return file.read()


# 4. Detect media type
def get_media_type(filepath: str, fallback: str) -> str:
    media_type, _ = mimetypes.guess_type(filepath)
    return media_type or fallback


# 5. Build prompt
def build_prompt(patient_text: str) -> str:
    return (
        "You are a skin-health assistant. "
        "Speak naturally, clearly, and reassuringly. "
        "Limit your response to two or three sentences maximum. "
        "Do not use markdown, asterisks, or decorative symbols. "
        "Do not claim a confirmed diagnosis from text, images, "
        "or videos alone. "
        "If symptoms appear urgent, recommend appropriate "
        "professional medical care. "
        "If an image is provided without a video, ask for a "
        "video only if additional visual information would help. "
        "You are an AI assistant, not a replacement for a "
        "qualified healthcare professional. "
        f"\n\nPatient text: {patient_text}"
    )


# 6. Main doctor brain function
def doctor_brain(
    patient_text: str,
    image_filepath: Optional[str] = None,
    video_filepath: Optional[str] = None,
) -> str:

    if not patient_text or not patient_text.strip():
        patient_text = "The patient has not provided a description."

    if image_filepath and video_filepath:
        raise ValueError(
            "Please provide either an image or a video, not both."
        )

    prompt = build_prompt(patient_text)

    # 7. Text-only analysis
    if not image_filepath and not video_filepath:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )

        return response.text or "No response generated."

    # 8. Video + text analysis
    if video_filepath:
        video_path = Path(video_filepath).expanduser().resolve()

        if not video_path.is_file():
            raise FileNotFoundError(
                f"Video not found: {video_path}"
            )

        video_file = None

        try:
            print("Uploading video...")

            video_file = client.files.upload(
                file=str(video_path)
            )

            while (
                video_file.state
                and video_file.state.name == "PROCESSING"
            ):
                print("Video is processing...")
                time.sleep(2)

                video_file = client.files.get(
                    name=video_file.name
                )

            if (
                not video_file.state
                or video_file.state.name != "ACTIVE"
            ):
                state = (
                    video_file.state.name
                    if video_file.state
                    else "UNKNOWN"
                )

                raise RuntimeError(
                    f"Video processing failed. State: {state}"
                )

            print("Video ready. Analyzing...")

            response = client.models.generate_content(
                model=MODEL,
                contents=[
                    video_file,
                    prompt,
                ],
            )

            return response.text or "No response generated."

        finally:
            if video_file is not None:
                try:
                    client.files.delete(
                        name=video_file.name
                    )
                    print("Temporary video file deleted.")

                except Exception as cleanup_error:
                    print(
                        "Video cleanup warning:",
                        cleanup_error,
                    )

    # 9. Image + text analysis
    image_path = Path(image_filepath).expanduser().resolve()

    if not image_path.is_file():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    mime_type = get_media_type(
        str(image_path),
        "application/octet-stream",
    )

    if not mime_type.startswith("image/"):
        raise ValueError(
            "Invalid image file. Please provide a valid image."
        )

    image_data = encode_file(str(image_path))

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(
                data=image_data,
                mime_type=mime_type,
            ),
            prompt,
        ],
    )

    return response.text or "No response generated."


# 10. Test the function
if __name__ == "__main__":

    # Test 1: Text only
    # result = doctor_brain(
    #     "What are common causes of dry skin?"
    # )

    # Test 2: Image + text
    # result = doctor_brain(
    #     "I have redness on my skin.",
    #     image_filepath=str(BASE_DIR / "sample-image.jpg"),
    # )

    # Test 3: Video + text
    result = doctor_brain(
        "Please describe the visible skin changes.",
        video_filepath=str(BASE_DIR / "sample-video.mp4"),
    )

    print("\n--- DERMAAI RESPONSE ---")
    print(result)
