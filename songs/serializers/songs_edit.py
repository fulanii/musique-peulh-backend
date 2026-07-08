from rest_framework import serializers

from songs.models import Song


class SongEditSerializer(serializers.Serializer):
    song_id = serializers.IntegerField()
    new_title = serializers.CharField()
    new_artist_name = serializers.CharField()


    def validate(self, data):
        song_id = data["song_id"]
        data["new_title"] = data["new_title"].title()
        data["new_artist_name"] = data["new_artist_name"].title()

        if (
            Song.objects.filter(
                title=data["new_title"], artist_name=data["new_artist_name"]
            )
            .exclude(id=song_id) # don't match the song we're editing
            .exists()
        ):
            raise serializers.ValidationError(
                {"detail": f"Artist '{data['new_artist_name']}' already has a song titled '{data['new_title']}'."}
            )

        return data
