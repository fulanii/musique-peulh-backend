from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from songs.models import Song
from songs.serializers import SongSerializer
from songs.throttles import SongDataRateThrottle


@extend_schema(tags=["songs"])
class SongDataView(RetrieveAPIView):
    """
    Retrieve a single song by its title.

    Looks up one song using the `title` provided in the URL path.

    Permissions:
        * IsAuthenticated (JWT) — a valid access token is required.

    Required fields:
        * title (URL path) — the exact title of the song to retrieve.

    Expected response (200 OK):
        A single serialized song (SongSerializer):
        {
            "id": <int>,
            "title": <str>,
            "artist_name": <str>,
            "duration": <str>,
            "audio_file": <str>,   # URL
            "cover_image": <str>,  # URL
            "uploaded_by": <str>,
            "upload_date": <str>
        }

    Errors:
        * 401 Unauthorized — missing or invalid access token.
        * 404 Not Found — no song exists with the given title.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [SongDataRateThrottle]

    serializer_class = SongSerializer
    queryset = Song.objects.all()
    lookup_field = "title"

    def get_object(self):
        title = self.kwargs.get(self.lookup_field)
        return Song.objects.get(title=title)
