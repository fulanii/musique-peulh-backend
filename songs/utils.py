import os, re
import boto3
from botocore.exceptions import NoCredentialsError, ClientError, EndpointConnectionError
import uuid
from django.conf import settings
from dotenv import load_dotenv
from mutagen.mp3 import MP3
from mutagen import MutagenError
from rest_framework.exceptions import ValidationError


# load .env file
load_dotenv()


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


def upload_do(audio_file, cover_file) -> dict[str, str]:
    """Mothod to upload song and images to Digital Ocean Spaces"""
    try:
        s3 = boto3.client(
            "s3",
            region_name="sfo3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        audio_filename = sanitize_filename(audio_file.name)
        cover_filename = sanitize_filename(cover_file.name)

        # Upload files to DO Spaces
        s3.upload_fileobj(
            audio_file,
            settings.AUDIO_FOLDER,
            audio_filename,
            ExtraArgs={"ACL": "public-read", "ContentType": audio_file.content_type},
        )

        s3.upload_fileobj(
            cover_file,
            settings.COVER_FOLDER,
            cover_filename,
            ExtraArgs={"ACL": "public-read", "ContentType": cover_file.content_type},
        )

        # Construct URLs
        audio_url = (
            f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AUDIO_FOLDER}/{audio_filename}"
        )
        cover_url = (
            f"{settings.AWS_S3_ENDPOINT_URL}/{settings.COVER_FOLDER}/{cover_filename}"
        )

        return {"audio_url": audio_url, "cover_url": cover_url}

    except NoCredentialsError:
        raise RuntimeError("Missing or invalid DigitalOcean Spaces credentials")
    except EndpointConnectionError:
        raise RuntimeError("Could not connect to DigitalOcean Spaces endpoint")
    except ClientError as e:
        raise RuntimeError(f"Spaces client error: {e.response['Error']['Message']}")
    except Exception as e:
        raise RuntimeError(f"Unexpected upload error: {str(e)}")


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


# TODO: pick random song cover from a databse of song covers


# TODO: Auto covert audio files to mp3
