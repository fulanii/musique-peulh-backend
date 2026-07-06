from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class RegisterRateThrottle(AnonRateThrottle):
    scope = "register"


class LoginRateThrottle(AnonRateThrottle):
    scope = "login"


class EmailVerificationRateThrottle(AnonRateThrottle):
    scope = "email_verification"


class ResendEmailVerificationRateThrottle(AnonRateThrottle):
    scope = "resend_email_verification"


class PasswordResetRequestRateThrottle(AnonRateThrottle):
    scope = "password_reset_request"


class PasswordResetRateThrottle(AnonRateThrottle):
    scope = "password_reset"
