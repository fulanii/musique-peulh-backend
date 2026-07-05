from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Song
from .serializer import SongSerializer, SongUploadSerializer
from .utils import get_audio_duration, upload_r2


@extend_schema(tags=["songs"])
class AllSongs(ListAPIView):
    """
    A view to get all songs
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Song.objects.all()
    serializer_class = SongSerializer


@extend_schema(tags=["songs"])
class ArtistSongs(ListAPIView):
    """
    A view to get all songs by an artist
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SongSerializer

    def get_queryset(self):
        artist_name = self.kwargs["artist_name"]
        return Song.objects.filter(artist_name=artist_name)


@extend_schema(tags=["songs-admin"])
class UploadedBySongs(ListAPIView):
    """
    A view to get all songs uploaded by a certain user
    - username
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    serializer_class = SongSerializer

    def get_queryset(self):
        uploaded_by = self.kwargs["uploaded_by"]
        return Song.objects.filter(uploaded_by=uploaded_by)


@extend_schema(tags=["songs"])
class GetSong(RetrieveAPIView):
    """
    A view to get a specific song using its title
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SongSerializer
    queryset = Song.objects.all()
    lookup_field = "title"

    def get_object(self):
        title = self.kwargs.get(self.lookup_field)
        return Song.objects.get(title=title)


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
class SongUpload(APIView):
    """
    Upload a song R2 cloudflare,
    save their URLs in the database.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    parser_classes = [MultiPartParser, FormParser]
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def post(self, request):
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
            return Response(
                {"error": f"Upload failed: {str(e)}"},
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

        return Response(save_serializer.data, status=status.HTTP_201_CREATED)
