import pytest

from django.urls import reverse
from rest_framework.test import APIClient

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


@pytest.mark.django_db
def test_song_upload():
    client = APIClient()

    url = reverse("upload")

    with open("test/assets/test_audio.mp3", "rb") as audio, open("test/assets/test_cover.avif", "rb") as cover:
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


def test_get_song(song):
    url = "/api/song/title/denke denke/"

    client = APIClient()

    response = client.get(url)

    assert response.status_code == 200
    assert response.data["title"] == "Denke Denke"
    assert response.data["artist_name"] == "Disco Fils"


def test_get_artist(song):
    url = "/api/song/artist/disco fils/"

    client = APIClient()

    response = client.get(url)

    assert response.status_code == 200
    assert "Denke Denke" in response.data[0]["title"]
    assert "Disco Fils" in response.data[0]["artist_name"]


def test_upload_by(song):
    url = "/api/song/upload_by/yassine/"

    client = APIClient()

    response = client.get(url)

    assert response.status_code == 200
    assert response.data[0]["uploaded_by"] == "Yassine"
    assert "Denke Denke" in response.data[0]["title"]
    assert "Disco Fils" in response.data[0]["artist_name"]