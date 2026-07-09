from django.urls import include, path

from songs.views import (
    AllSongsView,
    ArtistSongsView,
    PlaylistDetailView,
    PlaylistSongsDetailView,
    PlaylistSongsView,
    PlaylistsView,
    SongDataView,
    SongsEditView,
    SongUploadView,
    StreamView,
    UploadedByUserSongsView,
    YoutubeDownloadView,
)

urlpatterns = [
    path("", AllSongsView.as_view(), name="all_songs"),
    path("upload/", SongUploadView.as_view(), name="upload-songs"),
    path("titles/<str:title>/", SongDataView.as_view(), name="song"),
    path("artists/<str:artist_name>/", ArtistSongsView.as_view(), name="artist"),
    path("upload_by/<str:uploaded_by>/", UploadedByUserSongsView.as_view(), name="upload_by"),
    path("stream/<int:song_id>", StreamView.as_view(), name="streaming"),
    path("playlist/", PlaylistsView.as_view(), name="playlist"),
    path("playlist/<int:playlist_id>/", PlaylistDetailView.as_view(), name="playlist-detail"),
    path("playlist/<int:playlist_id>/songs/", PlaylistSongsView.as_view(), name="playlist-songs"),
    path("playlist/<int:playlist_id>/songs/<int:song_id>/", PlaylistSongsDetailView.as_view(), name="playlist-songs-detail"),
    path("edit/", SongsEditView.as_view(), name="song-edit"),
    path("yt-download/", YoutubeDownloadView.as_view(), name="yt-download"),
]
