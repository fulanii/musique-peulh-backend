import re

from rest_framework import serializers

from songs.models import Playlist, Song


# --- Create a playlist
class CreatePlaylistSerializer(serializers.Serializer):
    playlist_name = serializers.CharField()

    def validate_playlist_name(self, value):
        playlist_name = value.lower().strip()

        # Length check
        if len(playlist_name) < 3:
            raise serializers.ValidationError("Playlist Name can't be less than 3 characters.")

        if len(playlist_name) > 100:
            raise serializers.ValidationError("Playlist Name can't be longer than 100 characters.")

        return playlist_name


# --- Returning song(s) data
class PlaylistSongResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ["id", "title", "artist_name", "duration"]


# --- Returning playlist(s) data
class PlaylistResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ["id", "playlist_name", "playlist_owner_id", "created_date"]


# --- Update a playlist name
class PlaylistNameUpdateSerializer(serializers.Serializer):
    playlist_id = serializers.IntegerField()
    new_playlist_name = serializers.CharField()

    def validate_new_playlist_name(self, value):
        new_playlist_name = value.lower().strip()

        # Length check
        if len(new_playlist_name) < 3:
            raise serializers.ValidationError("Playlist Name can't be less than 3 characters.")

        if len(new_playlist_name) > 100:
            raise serializers.ValidationError("Playlist Name can't be longer than 100 characters.")

        return new_playlist_name
