# Video to Text Generator

## Overview
The **Video to Text Generator** is an application designed to extract textual content from video files by transcribing the audio. This tool is ideal for creating subtitles, analyzing spoken content, or converting video-based information into text format for further processing.

## Features
- **Supports multiple video formats** (e.g., MP4, AVI, MKV, MOV).
- **High-accuracy transcription** using advanced speech-to-text technology.
- **Customizable language support** for different audio inputs.
- **Easy-to-use interface** for selecting video files and processing them.
- **Output text file generation** in `.txt` or other formats as needed.

## Requirements
### Software:
- Python 3.8 or above.
- Operating System: Windows, macOS, or Linux.

### Dependencies:
- `ffmpeg` (for audio extraction)
- `ffprobe`
- `speech_recognition` (for transcription)
- `pydub` (for audio processing)

Install dependencies using:
```bash
pip install ffmpeg-python speechrecognition pydub
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/video-to-text-generator.git
   ```
2. Navigate to the project directory:
   ```bash
   cd video-to-text-generator
   ```
3. Ensure all dependencies are installed (refer to the Requirements section).

## Usage
1. Run the main script:
   ```
   python main.py
   ```
2. Use the application interface to:
   - Select the video file.
   - Choose the desired language for transcription.
   - Start the transcription process.
3. Retrieve the generated text file from the specified output directory.


## Customization
- **Language Support**: Modify the `language` parameter in the script to change transcription languages.
- **Output Directory**: Configure the default output path in the settings file.

## Limitations
- Background noise in videos may reduce transcription accuracy.
- Requires an active internet connection for cloud-based transcription services.


## License
This project is licensed under the [MIT License](LICENSE).

## Contact
For any inquiries or support, please contact [amitsarkar01377@gmail.com](mailto:amitsarkar01377@gmail.com).