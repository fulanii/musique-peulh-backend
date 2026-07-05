from rest_framework import serializers


class PasswordResetRequestSerialiazer(serializers.Serializer):
    email = serializers.EmailField()
