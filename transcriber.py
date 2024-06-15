import whisper
import argparse
from pydub import AudioSegment
import os
import time
import warnings
import sys

# Suppress specific warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def convert_to_wav(audio_path):
    if audio_path.lower().endswith('.mp3'):
        audio = AudioSegment.from_mp3(audio_path)
        wav_path = audio_path.replace('.mp3', '.wav')
        audio.export(wav_path, format="wav")
    elif audio_path.lower().endswith('.webm'):
        audio = AudioSegment.from_file(audio_path, format="webm")
        wav_path = audio_path.replace('.webm', '.wav')
        audio.export(wav_path, format="wav")
    elif audio_path.lower().endswith('.mp4'):
        audio = AudioSegment.from_file(audio_path, format="mp4")
        wav_path = audio_path.replace('.mp4', '.wav')
        audio.export(wav_path, format="wav")
    elif audio_path.lower().endswith('.wav'):
        wav_path = audio_path
    else:
        raise ValueError("The input file must be an MP3, WAV, WEBM, or MP4 file.")
    return wav_path

def transcribe_audio_with_whisper(wav_path, model_name, language, verbose):
    model = whisper.load_model(model_name)
    result = model.transcribe(wav_path, language=language, verbose=verbose)
    return result

def save_transcription(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    parser = argparse.ArgumentParser(description="Transcribe MP3, WAV, WEBM, or MP4 audio files to text.")
    parser.add_argument("input_file", help="Path to the MP3, WAV, WEBM, or MP4 file to transcribe")
    parser.add_argument("--language", default="es", help="Language of the audio for transcription (default=es)")
    parser.add_argument("--model", default="medium", help="Whisper model to use for transcription: tiny, base, small, medium, large (default=medium)")
    parser.add_argument("--output_format", default="txt", choices=['txt', 'srt', 'json'], help="Output format for the transcription (default=txt)")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output during transcription")
    args = parser.parse_args()

    audio_path = args.input_file
    if not (audio_path.lower().endswith('.mp3') or audio_path.lower().endswith('.wav') or 
            audio_path.lower().endswith('.webm') or audio_path.lower().endswith('.mp4')):
        raise ValueError("The input file must be an MP3, WAV, WEBM, or MP4 file.")

    # Convert to WAV if necessary
    wav_path = convert_to_wav(audio_path)

    try:
        # Transcribe the audio
        print("Starting transcription...")
        start_time = time.time()
        result = transcribe_audio_with_whisper(wav_path, args.model, args.language, args.verbose)
        text = result['text']
    except KeyboardInterrupt:
        print("\nTranscription interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Failed to transcribe audio: {e}")
        return
    end_time = time.time()

    # Save the transcription to the desired output format
    output_base_path = audio_path.rsplit('.', 1)[0]
    if args.output_format == 'txt':
        output_path = output_base_path + '.txt'
        save_transcription(text, output_path)
    elif args.output_format == 'srt':
        output_path = output_base_path + '.srt'
        with open(output_path, 'w', encoding='utf-8') as f:
            for segment in result['segments']:
                start = segment['start']
                end = segment['end']
                f.write(f"{segment['id']}\n")
                f.write(f"{format_time(start)} --> {format_time(end)}\n")
                f.write(f"{segment['text']}\n\n")
    elif args.output_format == 'json':
        import json
        output_path = output_base_path + '.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)

    # Clean up the WAV file if it was converted
    if audio_path.lower().endswith(('.mp3', '.webm', '.mp4')):
        os.remove(wav_path)

    # Print the summary
    duration = end_time - start_time
    num_words = len(text.split())
    print(f"Transcription saved to {output_path}")
    print(f"Transcription completed in {duration // 60} minutes and {duration % 60:.2f} seconds")
    print(f"Model used: {args.model}")
    print(f"Language: {args.language}")
    print(f"Output format: {args.output_format}")
    print(f"Number of words: {num_words}")

def format_time(seconds):
    """Format seconds to SRT time format"""
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

if __name__ == "__main__":
    main()
