import whisper

def audio_to_text(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    print("Transcription:\n")
    print(result["text"])
    return result['text']

if __name__ == "__main__":
    audio_path = r"C:\Users\megal\OneDrive\Desktop\AI_Video\audios\output.wav"
    text = audio_to_text(audio_path)
    
