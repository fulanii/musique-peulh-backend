from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets, status

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Song
from .utils import upload_do, get_audio_duration, upload_images, get_random_cover_url
from .serializer import SongSerializer, SongUploadSerializer, ImagesUploadSerializer


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
    Upload a song + cover image to DigitalOcean Spaces,
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

        # grab data from request
        title = request.data["title"]
        artist_name = request.data["artist_name"]
        audio_file = request.FILES["audio_file"]

        # get duraton
        duration = get_audio_duration(audio_file=audio_file)

        # upload audio file to digital ocean spaces
        try:
            urls = upload_do(audio_file=audio_file)
        except Exception as e:
            return Response(
                {"error": f"Upload failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        random_cover_image = get_random_cover_url()
        # save song info to db along side media urls
        new_song = Song.objects.create(
            title=title,
            artist_name=artist_name,
            duration=duration,
            uploaded_by=request.user.username,
            audio_file=urls["audio_url"],
            cover_image=random_cover_image,
        )

        # serialize data to return to client
        save_serializer = SongSerializer(new_song)

        return Response(save_serializer.data, status=status.HTTP_201_CREATED)


class UploadImages(APIView):
    """
    Mass upload song cover images to Digital Ocean Spaces
    - image: raw image(s) files
    """

    parser_classes = [MultiPartParser]
    serializer_class = ImagesUploadSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @extend_schema(
        request=ImagesUploadSerializer,
        responses={
            200: {"description": "File(s) uploaded successfully"},
            400: OpenApiResponse(description="Invalid data"),
        },
        tags=["songs-admin"],
    )
    def post(self, request, *args, **kwargs):
        serializer = ImagesUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        files = serializer.validated_data["files"]

        # upload to D.O
        if upload_images(files):
            return Response({"message": f"Successfully uploaded {len(files)} files."})
        else:
            return Response({"error": f"Something went wrong while uploading"})


# TODO: Create playlist logic creating/adding/removing songs urls/views
