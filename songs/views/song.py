from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from songs.models import Song
from songs.serializers import SongSerializer, SongUploadSerializer
from songs.utils import get_audio_duration, upload_r2


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
