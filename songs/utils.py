import os, re
import boto3
from botocore.exceptions import NoCredentialsError, ClientError, EndpointConnectionError
import uuid
from django.conf import settings


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
            "Songs",  # settings.AWS_STORAGE_BUCKET_NAME
            audio_filename,
            ExtraArgs={"ACL": "public-read", "ContentType": audio_file.content_type},
        )

        s3.upload_fileobj(
            cover_file,
            "SongsCovers",  # settings.AWS_STORAGE_BUCKET_NAME
            cover_filename,
            ExtraArgs={"ACL": "public-read", "ContentType": cover_file.content_type},
        )

        # Construct URLs
        audio_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{audio_filename}"
        cover_url = f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{cover_filename}"

        return {"audio_url": audio_url, "cover_url": cover_url}

    except NoCredentialsError:
        raise RuntimeError("Missing or invalid DigitalOcean Spaces credentials")
    except EndpointConnectionError:
        raise RuntimeError("Could not connect to DigitalOcean Spaces endpoint")
    except ClientError as e:
        raise RuntimeError(f"Spaces client error: {e.response['Error']['Message']}")
    except Exception as e:
        raise RuntimeError(f"Unexpected upload error: {str(e)}")
