from rest_framework import serializers

from songs.models import Song


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

    def validate(self, data):
        data["new_ttitleitle"] = data["title"].title()
        data["artist_name"] = data["artist_name"].title()

        if Song.objects.filter(title=data["title"], artist_name=data["artist_name"]).exists():
            raise serializers.ValidationError({"detail": f"Artist '{data['artist_name']}' already has a song titled '{data['title']}'."})

        return data
