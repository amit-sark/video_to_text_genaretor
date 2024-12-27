from pydub import AudioSegment
from pydub.utils import which


import time 

start_time = time.time()

# Specify the path to ffmpeg and ffprobe
AudioSegment.converter = which("./ffmpeg.exe")
AudioSegment.ffprobe = which("./ffprobe.exe")

# Extract audio from the video
audio = AudioSegment.from_file("videoplayback.mp4")
audio.export("audio.wav", format="wav")

end_time = time.time()

print(f"total={end_time-start_time}")

print("Audio extraction successful!")
