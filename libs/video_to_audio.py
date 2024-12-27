from pydub import AudioSegment
from pydub.utils import which
from speech_to_text import get_large_audio_transcription_parallel

import time 

start_time = time.time()

# Specify the path to ffmpeg and ffprobe
AudioSegment.converter = which("./ffmpeg.exe")
AudioSegment.ffprobe = which("./ffprobe.exe")


def convert_audio(path,image,indicator,writting_label):
    checker = None
    audio = AudioSegment.from_file(path)
    audio.export("audio.wav", format="wav")

    end_time = time.time()

    print(f"total={end_time-start_time}")

    print("Audio extraction successful!")
    indicator.configure(text="Audio extraction successful!")
    
    get_large_audio_transcription_parallel(path=path,indicator=indicator,image=image,writting_label=writting_label)
    checker==1
            