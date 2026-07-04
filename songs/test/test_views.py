import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import CustomUser
from songs.models import Song


@pytest.fixture
def song(db):
    return Song.objects.create(
        title="Denke Denke",
        artist_name="Disco Fils",
        duration=3.12,
        uploaded_by="Yassine",
        audio_file="https://fake-bucket/song.mp3",
        cover_image="https://fake-bucket/cover.jpg",
    )


@pytest.fixture
def login():
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

    # Make the user admin
    user = CustomUser.objects.get(email=register_data["email"])
    user.is_staff = True
    user.is_superuser = True
    user.save()

    login_url = reverse("login")
    login_user = client.post(login_url, login_data, format="json")

    return login_user.data["access"]


@pytest.mark.django_db
def test_song_upload(login):
    client = APIClient(HTTP_AUTHORIZATION=f"Bearer {login}")

    url = reverse("upload")

    with open("test/assets/test_audio.mp3", "rb") as audio, open(
        "test/assets/test_cover.avif", "rb"
    ) as cover:
        data = {
            "title": "denke denke",
            "artist_name": "disco fils",
            "duration": 3.12,
            "upload_by": "Yassine",
            "audio_file": audio,
            "cover_image": cover,
        }

        response = client.post(url, data, format="multipart")

        assert response.status_code == 201


def test_get_song(song, login):
    url = "/api/songs/titles/denke denke/"

    client = APIClient(HTTP_AUTHORIZATION=f"Bearer {login}")

    response = client.get(url)

    assert response.status_code == 200
    assert response.data["title"] == "Denke Denke"
    assert response.data["artist_name"] == "Disco Fils"


def test_get_artist(song, login):
    url = "/api/songs/artists/disco fils/"

    client = APIClient(HTTP_AUTHORIZATION=f"Bearer {login}")

    response = client.get(url)

    assert response.status_code == 200
    assert "Denke Denke" in response.data[0]["title"]
    assert "Disco Fils" in response.data[0]["artist_name"]


def test_upload_by(song, login):
    url = "/api/songs/upload_by/yassine/"

    client = APIClient(HTTP_AUTHORIZATION=f"Bearer {login}")

    response = client.get(url)

    assert response.status_code == 200
    assert response.data[0]["uploaded_by"] == "Yassine"
    assert "Denke Denke" in response.data[0]["title"]
    assert "Disco Fils" in response.data[0]["artist_name"]


def test_all_songs(song, login):
    url = reverse("all_songs")

    client = APIClient(HTTP_AUTHORIZATION=f"Bearer {login}")

    response = client.get(url)

    assert response.status_code == 200
    assert response.data[0]["title"] == "Denke Denke"
    assert response.data[0]["artist_name"] == "Disco Fils"
    assert response.data[0]["duration"] == 3.12
    assert response.data[0]["uploaded_by"] == "Yassine"
    assert response.data[0]["audio_file"] == "https://fake-bucket/song.mp3"
    assert response.data[0]["cover_image"] == "https://fake-bucket/cover.jpg"
