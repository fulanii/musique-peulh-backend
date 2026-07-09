from rest_framework import serializers


# ------------------- For displaying video data (title, duration, channel name)
class YtDataResponseSerializer(serializers.Serializer):
    title = serializers.CharField(allow_null=True)
    duration = serializers.IntegerField(allow_null=True)
    duration_string = serializers.CharField(allow_null=True)
    channel = serializers.CharField(allow_null=True)
    thumbnail = serializers.URLField(allow_null=True)


# ------------------- For downloading video
class YtDownloadSerializer(serializers.Serializer):
    url = serializers.URLField()
    title = serializers.CharField()
    artist_name = serializers.CharField()
