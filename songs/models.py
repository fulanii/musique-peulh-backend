from django.db import models
from django.conf import settings


class SongModel(models.Model):
    title = models.CharField(max_length=255, unique=True)  # Denke Denke
    artist_name = models.CharField(max_length=255)  # Disco Fils
    duration = models.DurationField()  # stored as timedelta
    audio_file = models.URLField()
    cover_image = models.URLField()
    upload_date = models.DateTimeField(auto_now_add=True)  # auto set on create
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,  # keep song even if user is deleted
        null=True,
        blank=True,
        related_name="songs",
    )

    class Meta:
        ordering = ["-upload_date"]

    def __str__(self):
        return f"{self.title} by {self.artist_name}"
