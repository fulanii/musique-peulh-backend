from rest_framework import serializers
from .models import SongModel


class SongSerializer(serializers.ModelSerializer):
    upload_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
    uploaded_by = serializers.StringRelatedField(read_only=True)
    song_duration = serializers.SerializerMethodField()  # custom formatting

    class Meta:
        model = SongModel
        fields = "__all__"

    def get_song_duration(self, obj):
        # obj.song_duration stored as float, e.g. 3.14 minutes
        total_seconds = int(obj.song_duration * 60)
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes}:{seconds:02d}"  # e.g. 3:14
