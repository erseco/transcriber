# Transcriber

Transcriber is a simple Python script that converts audio files (MP3, WAV, WEBM, or MP4) to text using the OpenAI Whisper model. It supports multiple languages and output formats.

## Features

- Transcribe audio files in MP3, WAV, WEBM, or MP4 format.
- Supports multiple Whisper models: tiny, base, small, medium, large.
- Specify the language of the audio for accurate transcription.
- Output the transcription in different formats: TXT, SRT, JSON.
- Verbose mode for detailed transcription process.

## Requirements

- Python 3.7 or higher
- pydub
- ffmpeg
- whisper

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/erseco/transcriber.git
   cd transcriber
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```sh
   python3 -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

3. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

4. Make sure you have `ffmpeg` installed. You can download it from [here](https://ffmpeg.org/download.html) and follow the installation instructions for your operating system.

## Usage

```sh
python transcriber.py <input_file> [--language <language>] [--model <model>] [--output_format <format>] [--verbose]
```

### Arguments

- `<input_file>`: Path to the MP3, WAV, WEBM, or MP4 file to transcribe.
- `--language`: Language of the audio for transcription (default: `es` for Spanish).
- `--model`: Whisper model to use for transcription (default: `medium`). Options: `tiny`, `base`, `small`, `medium`, `large`.
- `--output_format`: Output format for the transcription (default: `txt`). Options: `txt`, `srt`, `json`.
- `--verbose`: Enable verbose output during transcription.

### Examples

Transcribe an MP3 file to a text file:
```sh
python transcriber.py ~/Downloads/audio.mp3 --language en --model small --output_format txt
```

Transcribe a WEBM file to a JSON file with verbose output:
```sh
python transcriber.py ~/Downloads/audio.webm --language fr --model large --output_format json --verbose
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
