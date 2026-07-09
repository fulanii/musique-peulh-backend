from yt_dlp import YoutubeDL

from songs.models import Song
from songs.utils import get_audio_duration, upload_r2


def download_and_upload(url: str):
    """
    download yt video as mp3

    upload to r2

    save to db
    """

    with YoutubeDL() as ydl:
        ydl.download(url)
