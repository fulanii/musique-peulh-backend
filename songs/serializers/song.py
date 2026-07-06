from rest_framework import serializers

from songs.models import Song


class SongSerializer(serializers.ModelSerializer):
    upload_date = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Song
        fields = ["id", "title", "artist_name", "duration", "upload_date", "uploaded_by"]  # "__all__"
