from rest_framework import serializers

from songs.models import Song


class SongUploadSerializer(serializers.Serializer):
    title = serializers.CharField()
    artist_name = serializers.CharField()
    upload_date = serializers.DateField(format="%Y-%m-%d", read_only=True)

    # file
    audio_file = serializers.FileField()

    def validate(self, data):
        ALLOWED_AUDIO_TYPES = ["audio/mpeg"]

        artist_name = data.get("artist_name").title()
        title = data.get("title").title()

        data["artist_name"] = artist_name
        data["title"] = title

        if Song.objects.filter(artist_name=artist_name, title=title).exists():
            raise serializers.ValidationError({"error": f"Artist '{artist_name}' already has a song titled '{title}'."})

        if data["audio_file"].content_type not in ALLOWED_AUDIO_TYPES:
            raise serializers.ValidationError(
                {"error": "Only MP3 audio files are allowed."},
            )

        return data
