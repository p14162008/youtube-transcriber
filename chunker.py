import os
import subprocess

def split_video_ffmpeg(input_path, chunk_len=10, output_dir="chunks"):
    os.makedirs(output_dir, exist_ok=True)
    cmd = [
        "ffmpeg", "-i", input_path,
        "-f", "segment", "-segment_time", str(chunk_len),
        "-c", "copy", f"{output_dir}/chunk_%03d.mp4"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return sorted(os.listdir(output_dir))
