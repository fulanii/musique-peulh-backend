from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from drf_spectacular.utils import extend_schema

from .models import SongModel
from .serializer import SongSerializer


@extend_schema(tags=["songs"])
class AllSongs(ListAPIView):
    """
    A view to get all songs
    """

    queryset = SongModel.objects.all()
    serializer_class = SongSerializer
