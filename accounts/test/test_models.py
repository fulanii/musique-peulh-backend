import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ValidationError

from accounts.models import CustomUser


@pytest.mark.django_db
class TestModels:
    def test_username_valid(self):
        user = CustomUser(email="a@b.com", username="v.ald_1")
        user.set_password("strongpass123")
        user.full_clean()
        user.save()
        assert CustomUser.objects.count() == 1

    def test_username_invalid_chars(self):
        user = CustomUser(email="a@b.com", username="invalid!@#")
        user.set_password("strongpass123")
        with pytest.raises(ValidationError):
            user.full_clean()
