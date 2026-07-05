import re

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "username": {"error_messages": {"max_length": "Username must be between 3 and 8 characters long."}},
        }

    def validate_username(self, value):
        # Normalize to lowercase
        username = value.lower().strip()

        # only letters, numbers, underscores, and dots
        if not re.match(r"^[a-zA-Z0-9_.]+$", username):
            raise serializers.ValidationError("Only letters, numbers, underscores, and dots are allowed.")

        # Length check
        if len(username) < 3 or len(username) > 8:
            raise serializers.ValidationError("Username must be between 3 to 8 characters long.")

        # Uniqueness check (case-insensitive)
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with this username already exists.")

        return username

    def validate_email(self, value):
        # Normalize to lowercase
        email = value.lower().strip()

        # Uniqueness check (case-insensitive)
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists.")

        return email

    def validate_password(self, value):
        try:
            validate_password(value, self.instance)
        except Exception as e:
            raise serializers.ValidationError({"password": list(e)})

        return value

    # using custom create so password gets hashed b4 saving in db
    def create(self, validated_data):
        email = self.validated_data["email"].lower().strip()
        username = self.validated_data["username"].lower().strip()

        user = CustomUser(email=email, username=username)
        user.set_password(validated_data["password"])  # hashes the password
        user.save()
        return user
