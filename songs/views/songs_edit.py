import logging

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from songs.models import Song
from songs.serializers import SongEditSerializer

logger = logging.getLogger(__name__)


@extend_schema(tags=["songs-admin"])
class SongsEditView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = SongEditSerializer

    def patch(self, request):
        """
        Update a song's title and artist name (admin only).

        Validates the payload, looks up the song by id, and updates its title
        and artist name.

        Permissions:
            * IsAuthenticated + IsAdminUser (JWT) — requires a valid access
            token for a staff/admin user.

        Required fields:
            * song_id — the ID of the song to update.
            * new_title — the new title for the song.
            * new_artist_name — the new artist name for the song.

        Expected response (200 OK):
            {"detail": "Song name updated."}

        Errors:
            * 400 Bad Request — invalid/missing fields (serializer validation).
            * 401 Unauthorized — missing or invalid access token.
            * 403 Forbidden — authenticated but not an admin user.
            * 404 Not Found — no song exists for the given id:
            {"detail": "Song not found."}
        """
        user = request.user

        updates = SongEditSerializer(data=request.data)
        updates.is_valid(raise_exception=True)

        validated_data = updates.validated_data

        song_id = validated_data.get("song_id")
        new_title = validated_data.get("new_title")
        new_artist_name = validated_data.get("new_artist_name")

        try:
            song_data = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            logger.info(f"song name or title couldn't be updated. ID: {song_id}")

            return Response({"detail": "Song not found."}, status=status.HTTP_404_NOT_FOUND)

        song_data.title = new_title
        song_data.artist_name = new_artist_name
        song_data.save()

        logger.info(f"Song name or title updated by {user.username}")

        return Response({"detail": "Song name updated."}, status=status.HTTP_200_OK)
