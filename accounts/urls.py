from django.urls import path, include
from .views import RegisterUser, LoginUser

urlpatterns = [
    path("auth/register/", RegisterUser.as_view(), name="register"),
    path("auth/login/", LoginUser.as_view(), name="login"),
]
