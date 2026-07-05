from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from songs.models import Song
from songs.serializers import SongSerializer


@extend_schema(tags=["songs"])
class ArtistSongsView(ListAPIView):
    """
    List all songs by a given artist.

    Filters songs by the `artist_name` provided in the URL path.

    Permissions:
        * IsAuthenticated (JWT) — a valid access token is required.

    Required fields:
        * artist_name (URL path) — the artist to filter songs by.

    Expected response (200 OK):
        A list of serialized songs (SongSerializer) for that artist;
        an empty list if the artist has no songs.

    Errors:
        * 401 Unauthorized — missing or invalid access token.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SongSerializer

    def get_queryset(self):
        artist_name = self.kwargs["artist_name"]
        return Song.objects.filter(artist_name=artist_name)
