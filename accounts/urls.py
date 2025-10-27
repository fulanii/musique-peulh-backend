from django.urls import path, include
from .views import (
    RegisterUserView,
    LoginUserView,
    EmailVerificationView,
    GetUserView,
    GetUsersView,
    UpdateToAdminView,
    DeleteUserView,
    ResendCodeView,
    PasswordResetRequestView,
    PasswordResetView,
)

urlpatterns = [
    # account related
    path("auth/register/", RegisterUserView.as_view(), name="register"),
    path("auth/login/", LoginUserView.as_view(), name="login"),
    path("auth/verify-email/", EmailVerificationView.as_view(), name="verify-email"),
    path("auth/resend-verification/", ResendCodeView.as_view(), name="resend-code"),
    path(
        "auth/reset-password-request/",
        PasswordResetRequestView.as_view(),
        name="reset-request",
    ),
    path("auth/reset-password/", PasswordResetView.as_view(), name="reset"),
    # user relates
    path("auth/user/", GetUserView.as_view(), name="user"),
    path("auth/users/", GetUsersView.as_view(), name="users"),
    path("auth/user/admin/", UpdateToAdminView.as_view(), name="update_admin"),
    path("auth/users/delete/<int:id>", DeleteUserView.as_view(), name="users"),
]
