# DermaAI — AI Skin Health Assistant

DermaAI is an AI-powered skin health assistant that combines voice input with skin images or videos to provide AI-generated skin health guidance.

The application uses speech recognition to transcribe patient audio, Google Gemini to analyze the provided information, and Deepgram to generate an audio response.

## Features

- **Voice Input:** Upload an audio recording or record your voice.
- **Skin Image Analysis:** Provide a skin image alongside your voice input.
- **Skin Video Analysis:** Provide a skin video alongside your voice input.
- **Speech-to-Text:** Transcribe patient audio using Groq Whisper.
- **AI-Powered Guidance:** Generate skin health guidance using Google Gemini.
- **Text-to-Speech:** Listen to the generated response using Deepgram.
- **Responsive UI:** A clean Gradio interface for desktop and mobile devices.

## Tech Stack

- Python
- Gradio
- Google Gemini API (`google-genai`)
- Groq API
- Deepgram API
- SpeechRecognition
- PyDub
- python-dotenv

## Project Structure

```text
dermaai/
├── main.py
├── doctor_brain.py
├── speech_to_text.py
├── text_to_speech.py
├── requirements.txt
├── .env
└── README.md
```

## Prerequisites

- Python 3.12
- Google Gemini API key
- Groq API key
- Deepgram API key

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/codewith-ibrahim/dermaai
cd dermaai
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add the API keys using the variable names expected by your Python modules.

```env
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
```

**Important:** These variable names must match the names used in your existing Python code. Never commit your `.env` file or expose API keys publicly.

### 5. Run the application

```bash
python main.py
```

Open the local Gradio URL shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

## How to Use

1. Open DermaAI in your browser.
2. Record your voice or upload an audio file describing your skin concern.
3. Optionally upload either a skin image or a skin video.
4. Click **Analyze Skin Concern**.
5. Review the speech transcript and AI-generated guidance.
6. Listen to the generated audio response.

**Note:** The application currently accepts either an image or a video per analysis, not both simultaneously.

## Deployment

DermaAI can be deployed to a Python-compatible hosting platform that supports Gradio applications, such as Render or Hugging Face Spaces.

For deployment:

1. Push the project files and `requirements.txt` to your Git repository.
2. Configure the required API keys as environment variables or platform secrets.
3. Use the appropriate Python build and application start commands for your hosting platform.
4. Test audio uploads, image/video inputs, API calls, and audio playback after deployment.

Do not upload your `.env` file, virtual environment, or API credentials to a public repository.

## Medical Disclaimer

DermaAI provides AI-generated skin health information for educational and informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.

AI-generated results may be inaccurate or incomplete. Consult a qualified healthcare professional for medical concerns. Seek urgent medical attention for severe or rapidly worsening symptoms.

## Future Improvements

- Improved error handling and user feedback
- Support for additional languages
- Enhanced accessibility and mobile experience
- Deployment monitoring and performance improvements

## Author

**Shaikh Muhammad Ibrahim**

- GitHub: [codewith-ibrahim](https://github.com/codewith-ibrahim)

---

Built with Python, Gradio, and AI APIs.