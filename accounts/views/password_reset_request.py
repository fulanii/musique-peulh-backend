import logging
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser, PasswordResetCode
from accounts.serializer import PasswordResetRequestSerialiazer
from accounts.throttles import PasswordResetRequestRateThrottle
from accounts.utils import generate_strong_6_digit_number, send_password_reset_code_email

logger = logging.getLogger(__name__)


@extend_schema(tags=["credentials"])
class PasswordResetRequestView(APIView):
    """
    Request a password reset code to be emailed to the user.

    Generates a new 6-digit code (valid 15 minutes), stores it via
    update-or-create so any previous code is replaced, and emails it to the
    user. To avoid leaking which emails exist, the response is the same
    generic message whether or not the account is found.

    Permissions:
        * AllowAny — open endpoint, no authentication required.

    Throttle:
        * 5/hour (scope "password_reset_request").

    Required fields:
        * email — the account's email address to send the reset code to

    Expected response (200 OK):
        {"message": "If this email exists, a reset code has been sent to verify yourself."}

    Errors:
        * 500 Internal Server Error — any unexpected failure:
        {"detail": "An unexpected error occurred, while requesting password reset code.", "error": <str>}
    """

    serializer_class = PasswordResetRequestSerialiazer
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRequestRateThrottle]

    def post(self, request):
        email = request.data["email"]

        try:
            # check if user exist
            user_data = CustomUser.objects.get(email=email)

            # Generate and save a new code if doesnt exist update otherwise
            verification_code = generate_strong_6_digit_number()

            verification_instance, created = PasswordResetCode.objects.update_or_create(
                user=user_data,
                defaults={
                    "code": verification_code,
                    "expires_at": timezone.now() + timedelta(minutes=15),
                },
            )

            if not send_password_reset_code_email(
                code=str(verification_code),
                email=email,
                username=user_data.username,
            ):
                logger.warning(f"Password reset email sending fail for user: {user_data.username}")
            else:
                logger.info(f"Password reset email sent successfully: {user_data.username}")

            return Response(
                {"detail": "If this email exists, a reset code has been sent to verify yourself."},
                status=status.HTTP_200_OK,
            )

        except ObjectDoesNotExist:
            logger.info(f"Non existing account tried to request password reset: {email}")
            return Response(
                {"detail": "If this email exists, a reset code has been sent to verify yourself."},
                status=200,
            )

        except Exception as e:
            logger.error(f"Error ocured while requesting password reset: {email}, {e}")
            return Response(
                {
                    "detail": "An unexpected error occurred, while requesting password reset code.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
