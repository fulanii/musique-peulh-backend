from django.urls import path, include
from .views import (
    AllSongs,
    SongUpload,
    GetSong,
    ArtistSongs,
    UploadedBySongs,
    UploadImages,
)

urlpatterns = [
    path("songs/", AllSongs.as_view(), name="all_songs"),
    path("songs/upload/", SongUpload.as_view(), name="upload"),
    path("songs/upload/images", UploadImages.as_view(), name="upload"),
    path("songs/titles/<str:title>/", GetSong.as_view(), name="song"),
    path("songs/artists/<str:artist_name>/", ArtistSongs.as_view(), name="artist"),
    path(
        "songs/upload_by/<str:uploaded_by>/",
        UploadedBySongs.as_view(),
        name="upload_by",
    ),
]
