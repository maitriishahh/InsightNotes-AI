import yt_dlp
import os
from datetime import datetime
import re

audio_dir = "storage/audio"

def download_yt_audio(yt_url: str):
    """
    Downloads audio from YouTube URL.
    Returns (audio_file_path, video_title)
    """

    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    ydl_op = {
        "format": "bestaudio",
        "outtmpl": f"{audio_dir}/%(title)s.%(ext)s",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_op) as ydl:
            info = ydl.extract_info(yt_url, download=True)
            filename = ydl.prepare_filename(info)

        return filename, info["title"]

    except Exception as e:
        return None, str(e)

    

def extract_video_id(url:str):
    pattern = r"(?:v=|youtu\.be/|embed/|shorts/)([a-zA-Z0-9_-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None