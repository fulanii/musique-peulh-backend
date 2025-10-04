from django.urls import path, include
from .views import RegisterUser, LoginUser, Verification

urlpatterns = [
    path("auth/register/", RegisterUser.as_view(), name="register"),
    path("auth/login/", LoginUser.as_view(), name="login"),
    path("auth/verify-email/", Verification.as_view(), name="verify"),
]
