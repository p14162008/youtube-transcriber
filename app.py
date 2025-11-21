"""Fusion Frame: download a YouTube video, chunk it, and transcribe it in parallel."""
import sys

import torch

from chunker import split_video_ffmpeg
from downloader import download_youtube_video
from transcriber import transcribe_all_chunks


def fusion_frame_run(youtube_url: str) -> str:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Running on {device} for transcription.")

    print("Downloading video...")
    path = download_youtube_video(youtube_url)

    print("Splitting video into chunks...")
    split_video_ffmpeg(path)

    print("Transcribing chunks in parallel...")
    transcripts = transcribe_all_chunks("chunks")
    combined = " ".join(transcripts)

    print("\n=== TRANSCRIPT ===\n")
    print(combined)
    return combined


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py <youtube_url>")
        sys.exit(1)
    fusion_frame_run(sys.argv[1])
