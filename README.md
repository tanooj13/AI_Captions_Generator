
# AI Subtitles Generator

This Streamlit app allows you to upload a video file, extract the audio, transcribe the audio to text using OpenAI's Whisper model, generate subtitles, and burn those subtitles into the video. Additionally, the app can summarize the transcribed text using the Groq API.

## Features

- **Audio Extraction**: Extracts audio from a video file.
- **Audio Transcription**: Uses Whisper AI to transcribe audio to text.
- **Subtitle Generation**: Converts the transcription into subtitles in SRT format.
- **Burn Subtitles into Video**: Uses `ffmpeg` to burn the subtitles into the video.
- **Video Summarization**: Summarizes the transcribed text using Groq API.

## Installation

To run this project locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-subtitles-generator.git
cd ai-subtitles-generator
```

### 2. Set up the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install `ffmpeg`:

- **Windows**: Download `ffmpeg` from [ffmpeg.org](https://ffmpeg.org/download.html), extract it, and add the `bin` folder to your system's PATH.
- **macOS**: Use Homebrew to install `ffmpeg`:
  ```bash
  brew install ffmpeg
  ```
- **Linux**: Use your package manager to install `ffmpeg`:
  ```bash
  sudo apt install ffmpeg
  ```

### 5. Set up environment variables

Create a `.env` file in the root of the project directory and add your Groq API key:

```
GROQ_API_KEY=your-groq-api-key
```

Alternatively, you can set the `GROQ_API_KEY` using Streamlit secrets if deploying on Streamlit Cloud.

### 6. Run the app

Start the app with the following command:

```bash
streamlit run app.py
```

## Usage

- **Upload a Video**: Choose a video file (mp4 or mov format) to upload.
- **Generate Subtitles**: Click on the "Generate Subtitles" button to start the process of extracting audio, transcribing it, generating subtitles, and burning them into the video.
- **Summarize the Video**: Click on the "Summarize" button to summarize the transcribed text using the Groq API.

## Dependencies

- **Streamlit**: Web app framework for building interactive interfaces.
- **Whisper**: OpenAI's Whisper model for speech-to-text transcription.
- **MoviePy**: For video editing (audio extraction and burning subtitles).
- **Groq**: Used for text summarization via their API.
- **FFmpeg**: A tool for video processing.
- **Requests**: For making API requests.


