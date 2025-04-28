from moviepy.editor import VideoFileClip
import os

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
        else:
            print("No audio found in the video file.")
    except Exception as e:
        print(f"Error occurred while extracting the audio: {e}")


if __name__ == "__main__":
    video_path = r"C:\Users\megal\OneDrive\Desktop\AI_Video\videos\videoplayback.mp4"
    audio_output_path = r"C:\Users\megal\OneDrive\Desktop\AI_Video\audios\output.wav"
    os.makedirs(os.path.dirname(audio_output_path), exist_ok=True)
    extract_audio(video_path, audio_output_path)

    