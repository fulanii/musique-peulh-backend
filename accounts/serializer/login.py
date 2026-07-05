import re

from django.contrib.auth import authenticate
from rest_framework import serializers

from accounts.models import CustomUser


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError("Both identifier and password are required.")

        if "@" in identifier:
            email = identifier.lower().strip()
            try:
                user_obj = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid email or password.")
        else:
            try:
                username = identifier.lower().strip()
                user_obj = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("Invalid username or password.")

        # get user data based on email/username
        user = authenticate(
            request=self.context.get("request"),
            email=user_obj.email,
            password=attrs["password"],
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        attrs["user"] = user
        return attrs
