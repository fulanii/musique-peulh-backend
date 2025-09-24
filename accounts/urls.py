from django.urls import path, include
from .views import RegisterUser, LoginUser

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="user registration"),
    path("login/", LoginUser.as_view(), name="user login"),
]
