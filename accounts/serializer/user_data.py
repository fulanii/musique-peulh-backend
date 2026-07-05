from rest_framework import serializers

from accounts.models import CustomUser


class GetUserIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "username",
            "is_superuser",
            "is_staff",
            "is_active",
            "is_verified",
        ]
