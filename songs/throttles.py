from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class SongUpload(UserRateThrottle):
    scope = "song_upload"


class SongsRateThrottle(UserRateThrottle):
    scope = "songs"


class ArtistSongsRateThrottle(UserRateThrottle):
    scope = "artist_songs"


class UserUploadsRateThrottle(UserRateThrottle):
    scope = "user_uploads"


class SongDataRateThrottle(UserRateThrottle):
    scope = "song_data"


class StreamRateThrottle(UserRateThrottle):
    scope = "stream"


# ------------ Playlist (UserRateThrottle)
class PlaylistCreationRateTrottle(UserRateThrottle):
    scope = "create-playlist"


class PlaylistListRateTrottle(UserRateThrottle):
    scope = "get-playlists"


class PlaylistUpdateRateTrottle(UserRateThrottle):
    scope = "update-playlist"


class PlaylistDeleteRateTrottle(UserRateThrottle):
    scope = "delete-playlist"


class PlaylistSongsRateTrottle(UserRateThrottle):
    scope = "get-playlist-songs"


class PlaylistSongsAddRateTrottle(UserRateThrottle):
    scope = "add-playlist-song"


class PlaylistSongsRmvRateTrottle(UserRateThrottle):
    scope = "rmv-playlist-song"
