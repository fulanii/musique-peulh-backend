from songs.utils import upload_r2, get_audio_duration
from songs.models import Song
from yt_dlp import YoutubeDL


def download_and_upload(url: str, title: str, artist_name: str):
    """ 
    download yt video as mp3

    upload to r2

    save to db
    """

    with YoutubeDL() as ydl:
        ydl.download(url)