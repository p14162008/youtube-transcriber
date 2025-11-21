# Fusion Frame Pipeline

A small, fast YouTube → transcript pipeline. Give it a URL, and it downloads the video, splits it into chunks with `ffmpeg`, speeds the audio up 1.5×, and transcribes all chunks **in parallel** with `faster-whisper` (CUDA if available, CPU fallback).

## How it works

```
YouTube URL
    │
    ▼
downloader.py     ─ pytubefix downloads highest-res MP4
    │
    ▼
chunker.py        ─ ffmpeg segments into 10s chunks (-c copy, no re-encode)
    │
    ▼
transcriber.py    ─ ThreadPoolExecutor → faster-whisper("base", int8)
                    each chunk sped up 1.5× via pydub before inference
    │
    ▼
Combined transcript
```

The audio-speedup trick alone roughly halves transcription time with minimal accuracy loss on clean speech — useful for podcasts, lectures, and long-form video.

## Quick start

Prerequisites: Python 3.9+, `ffmpeg` on your `PATH`.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python app.py "https://www.youtube.com/watch?v=<id>"
```

The transcript is printed to stdout.

## Project layout

```
FusionFrame_AI/
├── app.py           # Entry point — orchestrates download → chunk → transcribe
├── downloader.py    # pytubefix wrapper
├── chunker.py       # ffmpeg segmenter
├── transcriber.py   # Parallel faster-whisper transcription
└── requirements.txt
```

## Notes / future work

- Defaults to the `base` Whisper model with `int8` quantization for a good size/quality trade-off. Swap to `small`, `medium`, or `large-v3` in `transcriber.py` for higher accuracy.
- Chunk length (currently 10s) is tuned for podcast-style content. Long sentences crossing chunk boundaries can fragment.
- A summarization stage was prototyped (BART, dynamic chunking) and removed pending a better model choice — see commit history.
