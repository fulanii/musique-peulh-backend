from django.urls import path, include
from .views import AllSongs, SongUpload, GetSong, ArtistSongs, UploadedBySongs

urlpatterns = [
    path("song/upload/", SongUpload.as_view(), name="all_songs"),
    path("songs/", AllSongs.as_view(), name="all_songs"),
    path("song/title/<str:title>/", GetSong.as_view(), name="song"),
    path("song/artist/<str:artist_name>/", ArtistSongs.as_view(), name="artist"),
    path("song/upload_by/<str:uploaded_by>/", UploadedBySongs.as_view(), name="artist"),
]
