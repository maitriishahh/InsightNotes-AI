import os
import subprocess

def extract_audio(video_path):
    audio_path = video_path.replace(".mp4", ".mp3")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "mp3",
        audio_path,
        "-y"
    ]

    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return audio_path
