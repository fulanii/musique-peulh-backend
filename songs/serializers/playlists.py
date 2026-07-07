import re

from rest_framework import serializers

from songs.models import Playlist, Song


class CreatePlaylistSerializer(serializers.Serializer):
    playlist_name = serializers.CharField()

    def validate_playlist_name(self, value):
        playlist_name = value.lower().strip()

        # Length check
        if len(playlist_name) < 3:
            raise serializers.ValidationError("Playlist Name can't be less than 3 characters.")

        if len(playlist_name) > 255:
            raise serializers.ValidationError("Playlist Name can't be loger than 255 characters.")

        return playlist_name


class PlaylistSongResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title", "artist_name", "duration"]


class PlaylistResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["id", "playlist_name", "playlist_owner_id", "created_date"]
