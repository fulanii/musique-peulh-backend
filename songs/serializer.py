from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from datetime import datetime
from .models import Song


class SongSerializer(serializers.ModelSerializer):
    upload_date = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Song
        fields = "__all__"


class SongUploadSerializer(serializers.Serializer):
    title = serializers.CharField()
    artist_name = serializers.CharField()
    duration = serializers.FloatField()
    audio_file = serializers.FileField()
    cover_image = serializers.ImageField()
    uploaded_by = serializers.CharField()
    upload_date = serializers.DateField(format="%Y-%m-%d", read_only=True)
