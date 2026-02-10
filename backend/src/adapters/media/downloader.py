from yt_dlp import YoutubeDL
from pathlib import Path
import tempfile
import os

class MediaDownloader:
    def __init__(self, temp_dir=None):
        self.temp_dir = Path(temp_dir or tempfile.gettempdir())
        os.makedirs(self.temp_dir, exist_ok=True)
    async def download_audio(self, url, source):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'outtmpl': str(self.temp_dir / '%(id)s.%(ext)s'),
            'quiet': True, 'no_warnings': True, 'retries': 3,
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return self.temp_dir / f"{info['id']}.mp3", {"title": info.get('title'), "duration": info.get('duration'), "thumbnail": info.get('thumbnail')}
    def cleanup(self, path):
        if path and path.exists(): path.unlink()
