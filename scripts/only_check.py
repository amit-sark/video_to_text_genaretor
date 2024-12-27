import os
import speech_recognition as sr
from pydub import AudioSegment
import concurrent.futures
import time 

# Create a speech recognition object
r = sr.Recognizer()

def transcribe_audio_chunk(chunk_path):
    """
    Transcribes a single audio chunk.
    """
    try:
        with sr.AudioFile(chunk_path) as source:
            audio = r.record(source)
            return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "[Unintelligible]"
    except sr.RequestError as e:
        return f"[API Error: {e}]"

def get_large_audio_transcription_parallel(path, chunk_length_ms=30000):
    """
    Splits the large audio file into chunks of fixed length (in milliseconds),
    transcribes each chunk in parallel, and ensures that the chunks' transcription results are returned in order.
    """
    # Load the audio file
    sound = AudioSegment.from_file(path)
    
    # Split the audio into chunks of fixed length
    chunks = []
    start = 0
    while start < len(sound):
        end = min(start + chunk_length_ms, len(sound))
        chunk = sound[start:end]
        chunks.append(chunk)
        start = end
    
    # Create a directory to store audio chunks
    folder_name = "audio-chunks"
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # Save chunks as temporary audio files
    chunk_paths = []
    for i, chunk in enumerate(chunks):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        chunk.export(chunk_filename, format="wav")
        chunk_paths.append((i, chunk_filename))  # Keep track of chunk index for ordering
    
    # Use parallel processing to transcribe chunks, keeping track of order
    results = [None] * len(chunk_paths)  # To store results in correct order
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(transcribe_audio_chunk, path[1]): path[0] for path in chunk_paths}
        total_chunks = len(chunk_paths)
        
        for idx, future in enumerate(concurrent.futures.as_completed(futures)):
            # Get transcription result
            index = futures[future]
            results[index] = future.result()

            # Calculate and print progress percentage
            progress = (idx + 1) / total_chunks * 100
            print(f"Progress: {progress:.2f}%")
    
    # Combine transcriptions in the correct order
    full_transcription = " ".join(results)

    
    # Split the transcription into words and add new lines after every 25 words
    words = full_transcription.split()
    lines = [' '.join(words[i:i+25]) for i in range(0, len(words), 25)]
    formatted_transcription = "\n".join(lines)
    # Clean up temporary files
    for chunk_path in chunk_paths:
        os.remove(chunk_path[1])
    
    # Save the transcription to a txt file
    with open("transcription.txt", "w") as f:
        f.write(formatted_transcription)
    
    return formatted_transcription

# Path to your audio file
s = time.time()
audio_path = "audio.wav"
print("\nFull Transcription:\n", get_large_audio_transcription_parallel(audio_path))
e = time.time()

print(f"Time: {e - s:.2f} seconds")
