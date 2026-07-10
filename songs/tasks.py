import logging
import os
import shutil
import tempfile

from celery import shared_task
from django.conf import settings
from yt_dlp import YoutubeDL

from songs.models import Song
from songs.utils import get_audio_duration, r2_client, sanitize_filename

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=2)
def download_and_upload(self, url: str, title: str, artist_name: str, uploaded_by: str):
    """
    Download a YouTube video as mp3, upload it to Cloudflare R2, and save the Song.

    Runs in the background (Celery). Steps:
        1. Download the best audio and convert it to mp3 (yt-dlp + ffmpeg,
        equivalent to `yt-dlp <url> -t mp3`).
        2. Upload the resulting mp3 to R2.
        3. Create the Song record pointing at the uploaded object.

    NOTE: the worker running this task must have **ffmpeg** installed — the
    mp3 conversion is done by ffmpeg (YouTube serves Opus/AAC, not mp3).
    """
    tmpdir = tempfile.mkdtemp(prefix="ytdl_")

    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(tmpdir, "%(id)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        # 1. Download + convert to mp3
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # after post-processing the file ends in .mp3
            mp3_path = os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"

        # 2. Upload to R2
        duration = get_audio_duration(mp3_path)
        file_size = os.path.getsize(mp3_path)
        r2_key = f"{settings.AUDIO_FOLDER}/{sanitize_filename(f'{title}.mp3')}"

        s3 = r2_client()

        with open(mp3_path, "rb") as fh:
            s3.put_object(
                Bucket=settings.R2_BUCKET_NAME,
                Key=r2_key,
                Body=fh,
                ContentType="audio/mpeg",
                ContentLength=file_size,
            )

        # 3. Save to DB
        Song.objects.create(
            title=title,
            artist_name=artist_name,
            duration=duration,
            uploaded_by=uploaded_by,
            audio_url=r2_key,
        )

        logger.info(f"YouTube upload complete: '{title}' by '{artist_name}' (by {uploaded_by})")

    except Exception as exc:
        logger.error(f"YouTube download/upload failed for '{url}': {exc}")
        # Retry transient failures (network / YouTube hiccups); gives up after max_retries.
        raise self.retry(exc=exc, countdown=30)

    finally:
        # Always clean up temp files, even on failure.
        shutil.rmtree(tmpdir, ignore_errors=True)
