from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from datetime import datetime
from .models import Song


class SongSerializer(serializers.ModelSerializer):
    upload_date = serializers.DateField(format="%Y-%m-%d", read_only=True)

    class Meta:
        model = Song
        fields = "__all__"
