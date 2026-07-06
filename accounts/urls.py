from django.urls import include, path

from .views import (DeleteUserView, EmailVerificationView, GetUsersView,
                    GetUserView, LoginUserView, PasswordResetRequestView,
                    PasswordResetView, RegisterUserView, ResendCodeView,
                    UpdateToAdminView)

urlpatterns = [
    # account related
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", LoginUserView.as_view(), name="login"),
    path("verify-email/", EmailVerificationView.as_view(), name="verify-email"),
    path("resend-verification/", ResendCodeView.as_view(), name="resend-code"),
    path("reset-password-request/", PasswordResetRequestView.as_view(), name="reset-request"),
    path("reset-password/", PasswordResetView.as_view(), name="reset"),
    # user relates
    path("user/", GetUserView.as_view(), name="user"),
    path("users/", GetUsersView.as_view(), name="users"),
    path("user/admin/", UpdateToAdminView.as_view(), name="update_admin"),
    path("users/delete/<int:id>", DeleteUserView.as_view(), name="users"),
]
