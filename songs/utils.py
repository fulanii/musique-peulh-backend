import os, re, random
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


def upload_do(audio_file) -> dict[str, str]:
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
        # cover_filename = sanitize_filename(cover_file.name)

        # Upload files to DO Spaces
        s3.upload_fileobj(
            audio_file,
            settings.AUDIO_FOLDER,
            audio_filename,
            ExtraArgs={"ACL": "public-read", "ContentType": audio_file.content_type},
        )

        # s3.upload_fileobj(
        #     cover_file,
        #     settings.COVER_FOLDER,
        #     cover_filename,
        #     ExtraArgs={"ACL": "public-read", "ContentType": cover_file.content_type},
        # )

        # Construct URLs
        audio_url = (
            f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AUDIO_FOLDER}/{audio_filename}"
        )
        # cover_url = (
        #     f"{settings.AWS_S3_ENDPOINT_URL}/{settings.COVER_FOLDER}/{cover_filename}"
        # )

        return {"audio_url": audio_url}
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


def upload_images(files) -> bool:
    """Mothod to upload images to Digital Ocean Spaces"""
    try:
        s3 = boto3.client(
            "s3",
            region_name="sfo3",
            endpoint_url="https://sfo3.digitaloceanspaces.com",  # settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        for file in files:
            cover_filename = sanitize_filename(file.name)

            s3.upload_fileobj(
                file,
                settings.COVER_FOLDER,
                cover_filename,
                ExtraArgs={"ACL": "public-read", "ContentType": file.content_type},
            )

        return True
    except NoCredentialsError:
        raise RuntimeError("Missing or invalid DigitalOcean Spaces credentials")
    except EndpointConnectionError:
        raise RuntimeError("Could not connect to DigitalOcean Spaces endpoint")
    except ClientError as e:
        raise RuntimeError(f"Spaces client error: {e.response['Error']['Message']}")
    except Exception as e:
        raise RuntimeError(f"Unexpected upload error: {str(e)}")


def get_random_cover_url() -> str:
    """
    Return a random image URL from the SongsCovers folder in DigitalOcean Spaces.
    Raises descriptive errors and logs failures.
    """
    try:
        # Initialize S3 client
        s3 = boto3.client(
            "s3",
            region_name="sfo3",
            endpoint_url=settings.DO_DOWNLOAD_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        folder_prefix = f"{settings.COVER_FOLDER}/"

        # List all objects in the folder
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)

        # Handle empty or invalid response
        if "Contents" not in response or not response["Contents"]:
            raise ValueError("No files found in SongsCovers folder.")

        # Filter valid files (skip directory placeholders)
        object_keys = [
            obj["Key"] for obj in response["Contents"] if not obj["Key"].endswith("/")
        ]

        if not object_keys:
            raise ValueError("No valid image files found in SongsCovers folder.")

        # Pick a random one
        random_key = random.choice(object_keys)

        # Construct public URL
        random_url = f"{settings.AWS_S3_ENDPOINT_URL}/{random_key}"
        return random_url

    except NoCredentialsError:
        raise ValueError("Storage credentials missing. Please contact support.")
    except EndpointConnectionError:
        raise ConnectionError("Unable to reach the storage service. Try again later.")
    except ClientError as e:
        raise RuntimeError(
            f"Storage error: {e.response['Error'].get('Message', 'Unknown error')}"
        )
    except Exception as e:
        raise RuntimeError(f"Unexpected error fetching random cover image: {str(e)}")


# TODO 1: Finish Auto covert audio files to mp3
def conver_to_mp3(audio_file):
    """
    Takes any audio file and covert to mp3
        User Uploads File  →  DRF View
        →  Save file temporarily (/tmp)
        →  Convert to .mp3 using ffmpeg
        →  Upload final .mp3 to Spaces
        →  Delete temp file
        →  Save URL to DB
    """
