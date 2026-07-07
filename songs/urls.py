from django.urls import include, path

from songs.views import (
    AllSongsView,
    ArtistSongsView,
    PlaylistSongsView,
    PlaylistsView,
    SongDataView,
    SongUploadView,
    StreamView,
    UploadedByUserSongsView,
)

urlpatterns = [
    path("", AllSongsView.as_view(), name="all_songs"),
    path("upload/", SongUploadView.as_view(), name="upload-songs"),
    path("titles/<str:title>/", SongDataView.as_view(), name="song"),
    path("artists/<str:artist_name>/", ArtistSongsView.as_view(), name="artist"),
    path("upload_by/<str:uploaded_by>/", UploadedByUserSongsView.as_view(), name="upload_by"),
    path("stream/<int:song_id>", StreamView.as_view(), name="streaming"),
    path("playlist/", PlaylistsView.as_view(), name="playlist"),
    path("playlist/<int:playlist_id>/songs/", PlaylistSongsView.as_view(), name="playlist-songs"),
]
