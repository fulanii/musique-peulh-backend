from rest_framework import serializers


class ResendCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
