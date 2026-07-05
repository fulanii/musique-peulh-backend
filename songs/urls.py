from django.urls import include, path

from songs.views import AllSongs, ArtistSongs, GetSong, SongUpload, UploadedByUserSongs

urlpatterns = [
    path("", AllSongs.as_view(), name="all_songs"),
    path("upload/", SongUpload.as_view(), name="upload-songs"),
    path("titles/<str:title>/", GetSong.as_view(), name="song"),
    path("artists/<str:artist_name>/", ArtistSongs.as_view(), name="artist"),
    path("upload_by/<str:uploaded_by>/", UploadedByUserSongs.as_view(), name="upload_by"),
]
