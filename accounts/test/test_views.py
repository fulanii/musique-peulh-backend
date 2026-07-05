import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import CustomUser


@pytest.fixture
def user(db):
    return CustomUser.objects.create(email="test@example.com", username="test", verification_code=524469)


@pytest.mark.django_db
def test_user_can_register():
    client = APIClient()
    url = reverse("register")
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    }
    response = client.post(url, data, format="json")

    assert response.status_code == 201
    assert "id" in response.data
    assert response.data["email"] == data["email"]


@pytest.mark.django_db
def test_user_can_login():
    client = APIClient()

    register_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
    }
    login_data = {
        "email": "test@example.com",
        "password": "testpass123",
    }

    register_url = reverse("register")
    register_user = client.post(register_url, register_data, format="json")

    login_url = reverse("login")
    login_user = client.post(login_url, login_data, format="json")

    assert login_user.status_code == 200
    assert "refresh" in login_user.data
    assert "access" in login_user.data


@pytest.mark.django_db
def test_verification(user):
    client = APIClient()

    verify_url = reverse("verify")

    verify_data = {"email": "test@example.com", "code": 524469}

    response = client.post(verify_url, verify_data, format="json")

    assert response.status_code == 200
    assert response.data["detail"] == "Email verified. You can now log in."
