from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()
    new_password = serializers.CharField()

    def validate_new_password(self, value):
        try:
            validate_password(value, self.instance)
        except Exception as e:
            raise serializers.ValidationError({"password": list(e)})

        return value
