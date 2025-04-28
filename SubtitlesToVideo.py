import subprocess
import os


def subtitles_to_video(video_path, subtitles_path, output_path, ffmpeg_path):
    video_full_path = os.path.abspath(video_path)
    output_full_path = os.path.abspath(output_path)

    # Escape the subtitles path properly for Windows
    # subtitles_path_escaped = subtitles_path.replace("\\", "\\\\")
    
    cmd = f'"{ffmpeg_path}" -i "{video_full_path}" -vf subtitles="{subtitles_path}" "{output_full_path}"'
    
    print("Running command:")
    print(cmd)

    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"Subtitles added to video and saved to {output_full_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while adding subtitles: {e}")


if __name__ == '__main__':
    ffmpeg_path = r"C:\ffmpeg-2025-04-23-git-25b0a8e295-essentials_build\ffmpeg-2025-04-23-git-25b0a8e295-essentials_build\bin\ffmpeg.exe"
    video_path = "videos/videoplayback.mp4"
    subtitles_path = "captions/output.srt"
    output_path = "videos/output_video.mp4"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    subtitles_to_video(video_path, subtitles_path, output_path, ffmpeg_path)
