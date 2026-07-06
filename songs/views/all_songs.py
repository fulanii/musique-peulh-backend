from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from songs.models import Song
from songs.serializers import SongSerializer
from songs.throttles import SongsRateThrottle


@extend_schema(tags=["songs"])
class AllSongsView(ListAPIView):
    """
    List all songs in the library.

    Returns every song, serialized with SongSerializer.

    Permissions:
        * IsAuthenticated (JWT) — a valid access token is required.

    Required fields:
        * None — this is a GET request with no body.

    Expected response (200 OK):
        A list of serialized songs (SongSerializer):
        [
            {
                "id": <int>,
                "title": <str>,
                "artist_name": <str>,
                "duration": <str>,
                "audio_file": <str>,   # URL
                "uploaded_by": <str>,
                "upload_date": <str>
            },
            ...
        ]

    Errors:
        * 401 Unauthorized — missing or invalid access token.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [SongsRateThrottle]
    queryset = Song.objects.all()
    serializer_class = SongSerializer
