from rest_framework import serializers


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()
