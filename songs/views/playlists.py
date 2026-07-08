import logging

from django.conf import settings
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from songs.models import Playlist, Song
from songs.serializers import CreatePlaylistSerializer, PlaylistNameUpdateSerializer, PlaylistResponseSerializer, PlaylistSongResponseSerializer

logger = logging.getLogger(__name__)


# -------------------------- Playlist (GET, POST, PATCH)
@extend_schema(tags=["playlist"])
class PlaylistsView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = []

    @extend_schema(
        request=CreatePlaylistSerializer,
        responses={201: OpenApiResponse(description="Playlist created.")},
    )
    def post(self, request):
        """
        Create a new playlist owned by the requesting user.

        Validates the payload, then creates a Playlist with the given name and
        the current user as its owner.

        Permissions:
            * IsAuthenticated (JWT) — any authenticated user may create a playlist.

        Required fields:
            * playlist_name — the name of the playlist to create.

        Validation:
            * playlist_name: 3 to 255 characters

        Expected response (201 Created):
            {"detail": "Playlist created."}

        Errors:
            * 400 Bad Request — invalid/missing fields (serializer validation).
            * 401 Unauthorized — missing or invalid access token.
            * 500 Internal Server Error — any unexpected failure while creating:
            {"detail": "Something went wrong. Try again."}
        """
        user = request.user

        serializer = CreatePlaylistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        playlist_name = serializer.validated_data["playlist_name"]

        try:
            Playlist.objects.create(playlist_name=playlist_name, playlist_owner=user)

            logger.info(f"User: '{user.username}', created playlist: '{playlist_name}'")

            return Response({"detail": "Playlist created."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Something went wrong while creating the playlist: {e}")
            return Response({"detail": "Something went wrong. Try again."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=None, responses=PlaylistResponseSerializer(many=True))
    def get(self, request):
        """
        List all playlists owned by the requesting user.

        Returns every playlist whose owner is the current user.

        Permissions:
            * IsAuthenticated (JWT) — a valid access token is required.

        Required fields:
            * None — this is a GET request with no body.

        Expected response (200 OK):
            A list of the user's playlists, each with its songs nested
            (PlaylistResponseSerializer):
            [
                {
                    "id": <int>,
                    "playlist_name": <str>,
                    "playlist_owner_id": <int>,
                    "created_date": <str>,
                },
                ...
            ]

            If the user has no playlists, returns 200 with:
            {"detail": "User has no playlist."}

        Errors:
            * 401 Unauthorized — missing or invalid access token.
            * 500 Internal Server Error — any unexpected failure:
            {"detail": []}
        """
        user = request.user

        try:
            all_playlists = Playlist.objects.filter(playlist_owner=user)

            if not all_playlists.exists():
                return Response({"detail": []}, status=200)

            return Response(PlaylistResponseSerializer(all_playlists, many=True).data, status=200)

        except Exception as e:
            logger.error(f"Something went wrong while fetching user playlist: {e}")
            return Response({"detail": "Something went wrong."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        request=PlaylistNameUpdateSerializer,
        responses={200: OpenApiResponse(description="Playlist name updated.")},
    )
    def patch(self, request):
        """
        Rename a playlist owned by the requesting user.

        Validates the payload, looks up the playlist scoped to the current user,
        and updates its name. A playlist owned by someone else is treated as not
        found.

        Permissions:
            * IsAuthenticated (JWT) — a valid access token is required.
            * The requesting user must own the playlist.

        Required fields:
            * playlist_id — the ID of the playlist to rename.
            * new_playlist_name — the new name for the playlist.

        Expected response (200 OK):
            {"detail": "Playlist name updated."}

        Errors:
            * 400 Bad Request — invalid/missing fields (serializer validation).
            * 401 Unauthorized — missing or invalid access token.
            * 404 Not Found — no playlist with the given id belongs to the user:
            {"detail": "Playlist not found."}
        """
        user = request.user

        serializer = PlaylistNameUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_playlist_name = serializer.validated_data["new_playlist_name"]
        playlist_id = serializer.validated_data["playlist_id"]

        try:
            playlist_data = Playlist.objects.get(id=playlist_id, playlist_owner=user)
        except Playlist.DoesNotExist:
            return Response({"detail": "Playlist not found."}, status=404)

        playlist_data.playlist_name = new_playlist_name
        playlist_data.save()

        return Response({"detail": "Playlist name updated."}, status=status.HTTP_200_OK)


# -------------------------- Playlist Detail (DELETE)
@extend_schema(tags=["playlist"])
class PlaylistDetailView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = []

    def delete(self, request, playlist_id):
        """
        Delete a playlist owned by the requesting user.

        Looks up the playlist scoped to the current user and deletes it. A
        playlist owned by someone else is treated as not found.

        Permissions:
            * IsAuthenticated (JWT) — a valid access token is required.
            * The requesting user must own the playlist.

        Required fields:
            * playlist_id (URL path) — the ID of the playlist to delete.

        Expected response (200 OK):
            {"detail": "Playlist deleted."}

        Errors:
            * 401 Unauthorized — missing or invalid access token.
            * 404 Not Found — no playlist with the given id belongs to the user:
            {"detail": "Playlist not found."}
        """
        user = request.user

        try:
            playlist_data = Playlist.objects.get(id=playlist_id, playlist_owner=user)
        except Playlist.DoesNotExist:
            return Response({"detail": "Playlist not found."}, status=404)

        playlist_data.delete()

        return Response({"detail": "Playlist deleted."}, status=status.HTTP_200_OK)


# -------------------------- Playlist Songs (GET)
@extend_schema(tags=["playlist-songs"])
class PlaylistSongsView(APIView):

    serializer_class = PlaylistSongResponseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, playlist_id):
        """
        List all songs in a given playlist.

        Looks up the playlist by `playlist_id` and returns its songs. Access is
        restricted to the playlist's owner.

        Permissions:
            * IsAuthenticated (JWT) — a valid access token is required.
            * The requesting user must own the playlist.

        Required fields:
            * playlist_id (URL path) — the ID of the playlist whose songs to list.

        Expected response (200 OK):
            A list of the playlist's songs (PlaylistSongResponseSerializer):
            [
                {
                    "id": <int>,
                    "title": <str>,
                    "artist_name": <str>,
                    "duration": <str>
                },
                ...
            ]
            An empty list if the playlist has no songs.

        Errors:
            * 401 Unauthorized — missing or invalid access token.
            * 404 Not Found — no playlist with the given id belongs to the user
            (a playlist owned by someone else is treated as not found):
            {"detail": "Playlist not found."}
        """
        user = request.user

        try:
            # playlist = Playlist.objects.prefetch_related("songs").get(id=playlist_id)
            playlist = Playlist.objects.get(id=playlist_id, playlist_owner=user)
        except Playlist.DoesNotExist:
            return Response({"detail": "Playlist not found."}, status=404)

        songs = playlist.songs.all()

        return Response(PlaylistSongResponseSerializer(songs, many=True).data, status=200)


# -------------------------- Playlist Songs Detail (DELETE, PATCH)
@extend_schema(tags=["playlist-songs"])
class PlaylistSongsDetailView(APIView):

    permission_classes = [IsAuthenticated]
    throttle_classes = []

    @extend_schema(request=None, responses=None)
    def patch(self, request, playlist_id, song_id):
        """
        Add a song to a playlist owned by the requesting user.

        Looks up the playlist scoped to the current user and the song by id,
        then adds the song to the playlist. The add is idempotent — a song
        already in the playlist is silently kept (no duplicate, no error). A
        playlist owned by someone else is treated as not found.

        Permissions:
            * IsAuthenticated (JWT) — a valid access token is required.
            * The requesting user must own the playlist.

        Required fields:
            * playlist_id (URL path) — the playlist to add the song to.
            * song_id (URL path) — the song to add.

        Expected response (200 OK):
            {"detail": "Song added to playlist."}

        Errors:
            * 401 Unauthorized — missing or invalid access token.
            * 404 Not Found — no playlist with the given id belongs to the user,
            or no song exists for the given id:
            {"detail": "Playlist not found."} / {"detail": "Song not found."}
        """

        user = request.user

        try:
            playlist = Playlist.objects.get(id=playlist_id, playlist_owner=user)
        except Playlist.DoesNotExist:
            return Response({"detail": "Playlist not found."}, status=404)

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({"detail": "Song not found."}, status=404)

        # .add() is idempotent. A ManyToMany can't hold duplicates, so adding a song that's already
        # in the playlist is a silent no-op — no error, no duplicate row. You don't need to pre-check.
        playlist.songs.add(song)  # M2M add — writes the join-table row

        return Response({"detail": "Song added to playlist."}, status=status.HTTP_200_OK)

    def delete(self, request, playlist_id, song_id):
        """
        Remove a song from a playlist owned by the requesting user.

        Looks up the playlist scoped to the current user and the song by id,
        then removes the song from the playlist (drops the join-table row; the
        song itself is not deleted). A playlist owned by someone else is treated
        as not found.

        Permissions:
            * IsAuthenticated (JWT) — a valid access token is required.
            * The requesting user must own the playlist.

        Required fields:
            * playlist_id (URL path) — the playlist to remove the song from.
            * song_id (URL path) — the song to remove.

        Expected response (200 OK):
            {"detail": "Song removed from playlist."}

        Errors:
            * 401 Unauthorized — missing or invalid access token.
            * 404 Not Found — no playlist with the given id belongs to the user,
            or no song exists for the given id:
            {"detail": "Playlist not found."} / {"detail": "Song not found."}
        """

        user = request.user

        try:
            playlist = Playlist.objects.get(id=playlist_id, playlist_owner=user)
        except Playlist.DoesNotExist:
            return Response({"detail": "Playlist not found."}, status=404)

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response({"detail": "Song not found."}, status=404)

        # .remove() drops the M2M join row without deleting the Song itself.
        playlist.songs.remove(song)

        return Response({"detail": "Song removed from playlist."}, status=status.HTTP_200_OK)
