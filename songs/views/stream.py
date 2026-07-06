import logging

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from songs.models import Song
from songs.throttles import StreamRateThrottle
from songs.utils import r2_client

logger = logging.getLogger(__name__)


class StreamView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [StreamRateThrottle]
    serializer_class = None

    def get(self, request, song_id):
        """
        Return a short-lived pre-signed URL for streaming a song's audio.

        Looks up the song by `song_id`, then generates a Cloudflare R2
        pre-signed GET URL for its stored audio object. The URL is valid for
        30 minutes (1800s) and should be fetched right before playback.

        Permissions:
            * IsAuthenticated (JWT) — a valid access token is required.

        Required fields:
            * song_id (URL path) — the ID of the song to stream.

        Expected response (200 OK):
            {"url": "<pre-signed R2 URL>"}

        Errors:
            * 400 Bad Request — song_id missing:
            {"detail": "Song ID is required."}
            * 404 Not Found — no song exists for the given id:
            {"detail": "Song with id '<song_id>' does not exist."}
            * 500 Internal Server Error — URL generation failed:
            {"detail": "Something went wrong"}
        """

        if not song_id:
            return Response({"detail": "Song ID is required."}, status=400)

        try:
            song_data = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({"detail": f"Song with id '{song_id}' does not exist."}, status=404)

        s3_client = r2_client()

        try:
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.R2_BUCKET_NAME, "Key": song_data.audio_url},
                ExpiresIn=1800,  # URL expires in 30 minutes (1800 seconds)
            )
            return Response({"url": url}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Something went wrong while generating pre signed url: {str(e)}")
            return Response({"detail": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
