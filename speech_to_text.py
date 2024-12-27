import os
import speech_recognition as sr
from pydub import AudioSegment
import concurrent.futures
from PIL import Image
from customtkinter import CTkImage

# Ensure FFmpeg is configured for pydub (set path if necessary)
AudioSegment.ffmpeg = r"./ffmpeg.exe"  # Change this path if needed

# Create a speech recognition object
r = sr.Recognizer()

def transcribe_audio_chunk(chunk_path):
    """
    Transcribes a single audio chunk.
    """
    with sr.AudioFile(chunk_path) as source:
        audio = r.record(source)
        return r.recognize_google(audio)
   

def get_large_audio_transcription_parallel(path, indicator, image, writting_label, chunk_length_ms=30000):
    """
    Splits the large audio file into chunks of fixed length (in milliseconds),
    transcribes each chunk in parallel, and ensures that the chunks' transcription results are returned in order.
    """
    # Load the audio file
    indicator.configure(text='Please wait a while')
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
    
    # Update image to indicate progress
    image_pth = os.path.join(os.getcwd(), 'assets', 'images', 'writting.jpg')
    img = Image.open(image_pth)
    resized_img = img.resize((300, 250))
    ct_img = CTkImage(resized_img, size=(300, 250))  # Convert to CTkImage
    image.configure(image=ct_img)
    image.image = ct_img  # Store the image reference
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(transcribe_audio_chunk, path[1]): path[0] for path in chunk_paths}
        total_chunks = len(chunk_paths)
        
        for idx, future in enumerate(concurrent.futures.as_completed(futures)):
            index = futures[future]
            results[index] = future.result()

            # Calculate and print progress percentage
            progress = (idx + 1) / total_chunks * 100
            print(f"Progress: {progress:.2f}%")
            indicator.configure(text=f"Progress: {progress:.2f}%")
    
    # Combine transcriptions in the correct order
    full_transcription = " ".join(results)
    
    # Format transcription into lines
    words = full_transcription.split()
    lines = [' '.join(words[i:i+25]) for i in range(0, len(words), 25)]
    formatted_transcription = "\n".join(lines)
    
    # Clean up temporary files
    for chunk_path in chunk_paths:
        os.remove(chunk_path[1])
        
    # Truncate long transcriptions
    if len(words) > 200:
        words = words[:200] + ['.... ..']

    # Create lines with up to 25 words each
    lines2 = [' '.join(words[i:i+25]) for i in range(0, len(words), 15)]
    formatted_transcription2 = "\n".join(lines2)

    # Update the indicator
    indicator.configure(text="Transcoding complete!")
    
    image_pth = os.path.join(os.getcwd(), 'assets', 'images', 'complete.png')
    img = Image.open(image_pth)
    resized_img = img.resize((300, 250))
    ct_img = CTkImage(resized_img, size=(300, 250))  # Convert to CTkImage
    image.configure(image=ct_img)
    image.image = ct_img
    writting_label.configure(text=formatted_transcription2)
    
    # Save the transcription to a txt file
    with open("transcription.txt", "w") as f:
        f.write(formatted_transcription)
    
    return formatted_transcription
