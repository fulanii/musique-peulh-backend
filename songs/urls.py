from django.urls import path, include
from .views import AllSongs

urlpatterns = [
    path("songs/", AllSongs.as_view(), name="all_songs"),
]
