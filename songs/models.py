from django.db import models


class Song(models.Model):
    title = models.CharField(max_length=255, unique=True)
    artist_name = models.CharField(max_length=255)
    duration = models.FloatField()

    audio_file = models.URLField()
    cover_image = models.URLField()

    upload_date = models.DateField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=255)

    class Meta:
        ordering = ["-upload_date"]

    def __str__(self):
        return f"{self.title} by {self.artist_name}"

    def save(self, *args, **kwargs):
        self.title = self.title.title()
        super().save(*args, **kwargs)
