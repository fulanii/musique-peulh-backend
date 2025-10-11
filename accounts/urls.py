from django.urls import path, include
from .views import (
    RegisterUser,
    LoginUser,
    Verification,
    GetUser,
    GetUsers,
    UpdateToAdmin,
)

urlpatterns = [
    path("auth/register/", RegisterUser.as_view(), name="register"),
    path("auth/login/", LoginUser.as_view(), name="login"),
    path("auth/verify-email/", Verification.as_view(), name="verify"),
    path("auth/user/<int:id>", GetUser.as_view(), name="user"),
    path("auth/user/admin/<int:id>", UpdateToAdmin.as_view(), name="update_admin"),
    path("auth/users/", GetUsers.as_view(), name="users"),
]
