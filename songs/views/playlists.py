import logging

from django.conf import settings
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from songs.models import Playlist, Song
from songs.serializers import CreatePlaylistSerializer, PlaylistResponseSerializer, PlaylistSongResponseSerializer

logger = logging.getLogger(__name__)


@extend_schema(tags=["songs-playlist"])
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

    # @extend_schema(request=None, responses=None)
    # def patch(self, request):
    #     """
    #     update playlist || add song to it

    #     only users own playlist or an admin
    #     """

    # @extend_schema(request=None, responses=None)
    # def delete(self, request):
    #     """
    #     delete a playlist

    #     only users own playlist or an admin
    #     """


@extend_schema(tags=["songs-playlist"])
class PlaylistSongsView(APIView):
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
        * 403 Forbidden — the playlist exists but is not owned by the user:
        {"detail": "Not allowed."}
        * 404 Not Found — no playlist exists for the given id:
        {"detail": "Playlist not found."}
    """

    serializer_class = PlaylistSongResponseSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, playlist_id):
        user = request.user

        try:
            # playlist = Playlist.objects.prefetch_related("songs").get(id=playlist_id)
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response({"detail": "Playlist not found."}, status=404)

        if playlist.playlist_owner_id != user.id:
            return Response({"detail": "Not allowed."}, status=403)

        songs = playlist.songs.all()

        return Response(PlaylistSongResponseSerializer(songs, many=True).data, status=200)
