from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView

from drf_spectacular.utils import extend_schema

from .models import Song
from .serializer import SongSerializer


@extend_schema(tags=["songs"])
class AllSongs(ListAPIView):
    """
    A view to get all songs
    """

    queryset = Song.objects.all()
    serializer_class = SongSerializer


@extend_schema(tags=["songs"])
class SongUpload(CreateAPIView):
    """
    A view to get all songs
    """

    queryset = Song.objects.all()
    serializer_class = SongSerializer
