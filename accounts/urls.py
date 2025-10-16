from django.urls import path, include
from .views import (
    RegisterUser,
    LoginUser,
    Verification,
    GetUser,
    GetUsers,
    UpdateToAdmin,
    DeleteUser,
    ResendCode,
    PasswordResetRequest,
    PasswordReset,
)

urlpatterns = [
    # account related
    path("auth/register/", RegisterUser.as_view(), name="register"),
    path("auth/login/", LoginUser.as_view(), name="login"),
    path("auth/verify-email/", Verification.as_view(), name="verify"),
    path("auth/resend-verification/", ResendCode.as_view(), name="verify"),
    path(
        "auth/reset-password-request/",
        PasswordResetRequest.as_view(),
        name="reset-request",
    ),
    path("auth/reset-password/", PasswordReset.as_view(), name="reset"),
    # user relates
    path("auth/user/", GetUser.as_view(), name="user"),
    path("auth/users/", GetUsers.as_view(), name="users"),
    path("auth/user/admin/", UpdateToAdmin.as_view(), name="update_admin"),
    path("auth/users/delete/<int:id>", DeleteUser.as_view(), name="users"),
]
