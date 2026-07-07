from django.conf import settings
from django.db import models

from accounts.models import CustomUser


class SongQuerySet(models.QuerySet):
    def filter(self, *args, **kwargs):
        for field in ["title", "artist_name", "uploaded_by"]:
            if field in kwargs:
                kwargs[field] = kwargs[field].title()
        return super().filter(*args, **kwargs)


class SongManager(models.Manager):
    def get_queryset(self):
        return SongQuerySet(self.model, using=self._db)


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist_name = models.CharField(max_length=255)
    duration = models.FloatField()

    audio_url = models.URLField()

    upload_date = models.DateField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=255)

    objects = SongManager()

    class Meta:
        ordering = ["-upload_date"]

    def __str__(self):
        return f"{self.title} by {self.artist_name}"

    def save(self, *args, **kwargs):
        self.title = self.title.title()
        self.artist_name = self.artist_name.title()
        self.artist_name = self.artist_name.title()
        self.uploaded_by = self.uploaded_by.title()

        super().save(*args, **kwargs)


class Playlist(models.Model):
    playlist_name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song, related_name="playlists", blank=True)
    playlist_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="playlists")
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.playlist_name} by {self.playlist_owner}"
