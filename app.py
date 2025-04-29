import os
import subprocess
import streamlit as st
from datetime import timedelta
import whisper
import srt
from moviepy.editor import VideoFileClip
from groq import Groq
from dotenv import load_dotenv
import requests
import json


# Extracting the audio from the video file
def extract_audio(video_path,audio_output_path):
    '''
    Extracts audio from a video file and saves it as a .wav file
    video_path: str : Path to the video file
    output_path: str : Path to save the extracted audio file
    '''
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        if audio:
            audio.write_audiofile(audio_output_path)
            print(f"Audio extracted and saved to {audio_output_path}")
            return True
        else:
            st.error("No audio found in the video file.")
            return False
    except Exception as e:
        st.error(f"Error occurred while extracting the audio: {e}")
        return  False

# Transcribing the audio using Whisper
def transcribe(audio_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result
    except Exception as e:
        st.error(f"Error occurred during transcription: {e}")
        return None
    

# Generating subtitles from the transcription result
def convertToSubtitles(transcription_res):

    try:
        segments = transcription_res['segments']
        subtitles = []

        for i,segment in enumerate(segments):
            subtitle = srt.Subtitle(
                index = i+1,
                start = timedelta(seconds=segment['start']),
                end = timedelta(seconds=segment['end']),
                content = segment['text'].strip()
            )
            subtitles.append(subtitle)

        return srt.compose(subtitles)
    except Exception as e:
        st.error(f"Error occurred while converting to subtitles: {e}")
        return ""
    
# Burning subtitles into the video using ffmpeg
def subtitles_to_video(video_path, subtitles_path, output_path, ffmpeg_path):
    video_full_path = os.path.abspath(video_path)
    output_full_path = os.path.abspath(output_path)

    # Escape the subtitles path properly for Windows
    # subtitles_path_escaped = subtitles_path.replace("\\", "\\\\")
    
    cmd = f'"{ffmpeg_path}" -i "{video_full_path}" -vf subtitles="{subtitles_path}" "{output_full_path}"'

    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"Subtitles added to video and saved to {output_full_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while adding subtitles: {e}")
        return False
    

def main():
    st.title("AI Subtitles Generator")
    st.write("Upload a video file to add subtitles to it.")

    # File uploader for video file
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov"])
    if uploaded_file:
        video_path = "videos/videoplayback.mp4"
        os.makedirs(os.path.dirname(video_path), exist_ok=True)
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Video file uploaded successfully!")
        st.video(video_path)

        if st.button("Generate Subtitles"):
            # Extract audio from the video
            os.makedirs("audios", exist_ok=True)
            audio_output_path = "audios/output.wav"
            st.write("Extracting audio...")
            if not extract_audio(video_path, audio_output_path):
                return 
            # Transcribe the audio
            st.write("Transcribing audio...")
            transcribe_result  = transcribe(audio_output_path)
            if not transcribe_result:
                return
            st.write("Transcription completed!")
            # st.write(transcribe_result['text'])

            # Generate subtitles
            srt_content = convertToSubtitles(transcribe_result)
            if not srt_content:
                return
            os.makedirs("captions", exist_ok=True)
            with open("captions/output.srt", "w", encoding='utf-8') as f:
                f.write(srt_content)
            # st.success("Subtitles generated and saved to captions/output.srt")

            # Burn subtitles into the video
            ffmpeg_path = "ffmpeg"
            output_path = "videos/output_video.mp4"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            st.write("Burning subtitles into the video...")
            if subtitles_to_video(video_path, "captions/output.srt", output_path, ffmpeg_path):
                st.success("Subtitles burned into the video successfully!")
                st.video(output_path)

                # Add a download button for the video
                with open(output_path, "rb") as video_file:
                    video_bytes = video_file.read()
                    st.download_button(
                        label="Download Video with Subtitles",
                        data=video_bytes,
                        file_name="output_video.mp4",
                        mime="video/mp4"
                    )
            else:
                st.error("Failed to burn subtitles into the video.")

        load_dotenv()  # Load environment variables

        # GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
        if st.button("Summarize"):
            # Summarize the transcription result
            st.write("Summarizing...")
            os.makedirs("audios", exist_ok=True)
            audio_output_path = "audios/output.wav"
            st.write("Extracting audio...")
            if not extract_audio(video_path, audio_output_path):
                return 
            # Transcribe the audio
            st.write("Transcribing audio...")
            transcribe_result  = transcribe(audio_output_path)
            if not transcribe_result:
                return
            st.write("Transcription completed!")
            text = transcribe_result['text']
            # Using Groq for summarization
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "meta-llama/llama-4-scout-17b-16e-instruct", 
                "messages": [
                    {"role": "user", "content": f"Summarize this video text in simple English:\n\n{text}"}
                ],
                "temperature": 0.2,
                "max_tokens": 300
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                st.write(result['choices'][0]['message']['content'].strip())
            else:
                raise Exception(f"Groq API Error: {response.status_code} - {response.text}")
                    
    
            

if __name__ == "__main__":
    main()



