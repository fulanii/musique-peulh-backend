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
