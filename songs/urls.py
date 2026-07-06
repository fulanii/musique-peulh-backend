from django.urls import include, path

from songs.views import AllSongsView, ArtistSongsView, GetSongView, SongUploadView, StreamView, UploadedByUserSongsView

urlpatterns = [
    path("", AllSongsView.as_view(), name="all_songs"),
    path("upload/", SongUploadView.as_view(), name="upload-songs"),
    path("titles/<str:title>/", GetSongView.as_view(), name="song"),
    path("artists/<str:artist_name>/", ArtistSongsView.as_view(), name="artist"),
    path("upload_by/<str:uploaded_by>/", UploadedByUserSongsView.as_view(), name="upload_by"),
    path("stream/<int:song_id>", StreamView.as_view(), name="streaming"),
]
