import os
import random
import re
import uuid

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError, EndpointConnectionError, NoCredentialsError
from django.conf import settings
from dotenv import load_dotenv
from mutagen import MutagenError
from mutagen.mp3 import MP3
from rest_framework.exceptions import ValidationError

load_dotenv()


def r2_client() -> boto3.client:
    client = boto3.client(
        "s3",
        endpoint_url=settings.R2_URL,
        aws_access_key_id=settings.R2_ACCESS_KEY,
        aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )

    return client


def sanitize_filename(file_name: str) -> str:
    """
    Sanitize an uploaded filename:
    - Keep only letters, numbers, hyphens, underscores, and dots
    - Replace spaces with underscores
    - Lowercase everything
    - Prefix with UUID for uniqueness
    """
    base_name = os.path.basename(file_name)
    base_name = base_name.lower().replace(" ", "_")
    base_name = re.sub(r"[^a-z0-9._-]", "", base_name)

    return f"{uuid.uuid4()}_{base_name}"


def get_audio_duration(audio_file):
    """
    Extract audio file duration in minutes.seconds format.
    Raises ValidationError if file is invalid or unreadable.
    """
    try:
        audio = MP3(audio_file)
        duration_seconds = round(audio.info.length)
        minutes = duration_seconds // 60
        seconds = duration_seconds % 60
        return f"{minutes}.{seconds}"

    except MutagenError:
        raise ValidationError("Invalid or corrupt MP3 file.")
    except (AttributeError, OSError, TypeError):
        raise ValidationError("Could not read the audio file.")
    except Exception as e:
        raise ValidationError(f"Unexpected error reading audio: {str(e)}")


def upload_r2(audio_file, file_size) -> str:
    """Mothod to upload song to cloudflare R2"""

    try:
        audio_filename = sanitize_filename(audio_file.name)
        s3 = r2_client()
        r2_key = f"songs/{audio_filename}"

        s3.put_object(
            Bucket=settings.R2_BUCKET_NAME,
            Key=r2_key,
            Body=audio_file,
            ContentType=audio_file.content_type,
            ContentLength=file_size,
        )

        return r2_key

    except Exception as e:
        raise RuntimeError(f"Unexpected upload error: {str(e)}")
