from django.urls import path, include
from .views import AllSongs, SongUpload, GetSong

urlpatterns = [
    path("song/<title>/", GetSong.as_view(), name="song"),
    path("songs/", AllSongs.as_view(), name="all_songs"),
    path("song/upload/", SongUpload.as_view(), name="all_songs"),

]
