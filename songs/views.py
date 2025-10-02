from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .models import Song
from .utils import upload_do
from .serializer import SongSerializer, SongUploadSerializer


@extend_schema(tags=["songs"])
class AllSongs(ListAPIView):
    """
    A view to get all songs
    """

    queryset = Song.objects.all()
    serializer_class = SongSerializer


@extend_schema(tags=["songs"])
class ArtistSongs(ListAPIView):
    """
    A view to get all songs by an artist
    """

    serializer_class = SongSerializer

    def get_queryset(self):
        artist_name = self.kwargs["artist_name"]
        return Song.objects.filter(artist_name=artist_name)


@extend_schema(tags=["songs"])
class UploadedBySongs(ListAPIView):
    """
    A view to get all songs uploaded by a certain user

    - username
    """

    serializer_class = SongSerializer

    def get_queryset(self):
        uploaded_by = self.kwargs["uploaded_by"]
        return Song.objects.filter(uploaded_by=uploaded_by)


@extend_schema(tags=["songs"])
class GetSong(RetrieveAPIView):
    """
    A view to get a specific song using its title
    """

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
                "duration": {"type": "string"},
                "upload_by": {"type": "string"},
                "audio_file": {"type": "string", "format": "binary"},
                "cover_image": {"type": "string", "format": "binary"},
            },
        }
    },
    tags=["songs"],
)
class SongUpload(APIView):
    """
    Upload a song + cover image to DigitalOcean Spaces,
    save their URLs in the database.
    """

    parser_classes = [MultiPartParser, FormParser]
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def post(self, request):
        text_fields = ["title", "artist_name", "duration", "upload_by"]
        file_fields = ["audio_file", "cover_image"]

        missing = []

        for field in text_fields:
            if not request.data.get(field):
                missing.append(field)

        for field in file_fields:
            if not request.FILES.get(field):
                missing.append(field)

        if missing:
            return Response(
                {"error": f"Missing required field(s): {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        title = request.data["title"]
        artist_name = request.data["artist_name"]
        duration = request.data["duration"]
        uploaded_by = request.data["upload_by"]
        audio_file = request.FILES["audio_file"]
        cover_file = request.FILES["cover_image"]

        if Song.objects.filter(title=title).exists():
            return Response(
                {"error": f"Song with title '{title}' already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            urls = upload_do(audio_file=audio_file, cover_file=cover_file)
        except Exception as e:
            return Response(
                {"error": f"Upload failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        new_song = Song.objects.create(
            title=title,
            artist_name=artist_name,
            duration=duration,
            uploaded_by=uploaded_by,
            audio_file=urls["audio_url"],
            cover_image=urls["cover_url"],
        )

        serializer = SongSerializer(new_song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
