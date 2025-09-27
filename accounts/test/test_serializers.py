import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestSerializer:
    def test_email_invalid(self):
        client = APIClient()
        url = reverse("register")

        data = {
            "email": "@example.com",
            "username": "testuser",
            "password": "testpass123",
        }

        response = client.post(url, data, format="json")

        assert response.status_code == 400
        assert "email" in response.data
        assert response.data["email"][0] == "Enter a valid email address."

    def test_email_unique(self):
        client = APIClient()
        url = reverse("register")

        data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
        }

        client.post(url, data, format="json")
        response = client.post(url, data, format="json")

        assert response.status_code == 400
        assert "email" in response.data
        assert response.data["email"][0] == "user with this email already exists."

    # TODO: Add 1 login serializer test