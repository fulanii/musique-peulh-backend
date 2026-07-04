from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(
        unique=True,
        max_length=8,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_.]+$",
                message="Only letters, numbers, underscores and dots are allowed.",
            )
        ],
    )
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = "email"  # now use email to login
    REQUIRED_FIELDS = ["username"]  # required when creating superuser

    def __str__(self):
        return f"User with username: {self.username} and email: {self.email}"


class EmailVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(minutes=15)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Verification for {self.user.username}"

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at


class PasswordResetCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(minutes=15)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Verification for {self.user.username}"

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at
