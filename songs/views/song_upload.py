import logging

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from songs.models import Song
from songs.serializers import SongSerializer, SongUploadSerializer
from songs.throttles import SongUpload
from songs.utils import get_audio_duration, upload_r2

logger = logging.getLogger(__name__)


@extend_schema(
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "artist_name": {"type": "string"},
                "audio_file": {"type": "string", "format": "binary"},
                "cover_image": {"type": "string", "format": "binary"},
            },
        }
    },
    tags=["songs-admin"],
)
class SongUploadView(APIView):
    """
    Upload a song to Cloudflare R2 and save its record in the database.

    Validates the multipart upload, pushes the audio file to R2, computes the
    track duration, and creates a Song row storing the returned media URL and
    the uploading admin's username.

    Permissions:
        * IsAuthenticated + IsAdminUser (JWT) — requires a valid access token
        for a staff/admin user.

    Throttle:
        * 100/min (scope "song_upload").

    Content type:
        * multipart/form-data

    Required fields:
        * title — the song's title
        * artist_name — the artist's name
        * audio_file — the audio file to upload
        * cover_image — the cover image (optional, depending on serializer)

    Expected response (201 Created):
        The created song, serialized with SongSerializer.

    Errors:
        * 400 Bad Request — invalid/missing fields (serializer validation).
        * 401 Unauthorized — missing or invalid access token.
        * 403 Forbidden — authenticated but not an admin user.
        * 500 Internal Server Error — the R2 upload failed:
        {"detail": "Upload failed: <reason>"}
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [SongUpload]

    parser_classes = [MultiPartParser, FormParser]
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def post(self, request):
        user = request.user
        # validate data being uploaded
        upload_serializer = SongUploadSerializer(data=request.data)
        upload_serializer.is_valid(raise_exception=True)
        validated_data = upload_serializer.validated_data

        # grab data from request
        title = validated_data.get("title")
        artist_name = validated_data.get("artist_name")
        audio_file = validated_data.get("audio_file")
        file_size = audio_file.size

        # upload audio file to digital ocean spaces
        try:
            url = upload_r2(audio_file=audio_file, file_size=file_size)
        except Exception as e:
            logger.info(f"Error occured while up uploading song to r2: {e}")
            return Response(
                {"detail": f"Upload failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # get duraton
        duration = get_audio_duration(audio_file=audio_file)

        # save song info to db along side media urls
        new_song = Song.objects.create(
            title=title,
            artist_name=artist_name,
            duration=duration,
            uploaded_by=request.user.username,
            audio_url=url,
        )

        # serialize data to return to client
        save_serializer = SongSerializer(new_song)

        logger.info(f"New song '{title}' - '{artist_name}' uploaded by '{user.username}'")
        return Response(save_serializer.data, status=status.HTTP_201_CREATED)
