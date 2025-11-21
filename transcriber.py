import faster_whisper
import concurrent.futures
import torch
import os
from pydub import AudioSegment
import tempfile

# Load the Whisper model with CUDA if available
model = faster_whisper.WhisperModel("base", compute_type="int8", device="cuda" if torch.cuda.is_available() else "cpu")

# Function to speed up audio using pydub
def speed_up_audio(input_path, speed=1.5):
    audio = AudioSegment.from_file(input_path)
    new_frame_rate = int(audio.frame_rate * speed)
    sped_up = audio._spawn(audio.raw_data, overrides={"frame_rate": new_frame_rate})
    sped_up = sped_up.set_frame_rate(audio.frame_rate)

    # Save to a temporary WAV file
    tmpfile = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    sped_up.export(tmpfile.name, format="wav")
    return tmpfile.name  # Return path to sped-up audio

# Transcription function
def transcribe_file(path):
    try:
        print(f"Starting transcription for: {path}")
        sped_up_path = speed_up_audio(path, speed=1.5)
        segments, _ = model.transcribe(sped_up_path, beam_size=5)
        transcript = " ".join([seg.text for seg in segments])
        print(f"Finished transcription for: {path}")
        return transcript
    except Exception as e:
        print(f"Error transcribing {path}: {e}")
        return ""
    finally:
        # Always delete the temp sped-up file
        if 'sped_up_path' in locals() and os.path.exists(sped_up_path):
            os.remove(sped_up_path)

# Process all chunks in parallel
def transcribe_all_chunks(folder):
    files = [f"{folder}/{f}" for f in os.listdir(folder)]

    if not files:
        print("❌ No files found in the chunks folder.")
        return []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(transcribe_file, files))

    return results
