from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


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
    verification_code = models.IntegerField(null=True)
    USERNAME_FIELD = "email"  # now use email to login
    REQUIRED_FIELDS = ["username"]  # required when creating superuser

