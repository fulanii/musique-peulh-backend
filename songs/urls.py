from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AllSongs, ArtistSongs, GetSong, SongUpload, UploadedBySongs

router = DefaultRouter()

urlpatterns = [
    path("songs/", AllSongs.as_view(), name="all_songs"),
    path("songs/upload/", SongUpload.as_view(), name="upload-songs"),
    path("songs/titles/<str:title>/", GetSong.as_view(), name="song"),
    path("songs/artists/<str:artist_name>/", ArtistSongs.as_view(), name="artist"),
    path(
        "songs/upload_by/<str:uploaded_by>/",
        UploadedBySongs.as_view(),
        name="upload_by",
    ),
]
