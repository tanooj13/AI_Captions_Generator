import whisper
import srt
from datetime import timedelta

def transcribe(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result

def convertToSubtitles(transcription_res):
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


if __name__ == '__main__':
    audio_file = r"C:\Users\megal\OneDrive\Desktop\AI_Video\audios\output.wav"
    transcription_res = transcribe(audio_file)
    srt_content = convertToSubtitles(transcription_res)

    with open(r"captions\output.srt","w", encoding='utf-8') as f:
        f.write(srt_content)
    print("Subtitles generated and saved to captions/output.srt")

