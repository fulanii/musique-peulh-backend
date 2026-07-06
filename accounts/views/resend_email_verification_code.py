import logging
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser, EmailVerification
from accounts.serializer import ResendCodeSerializer
from accounts.throttles import ResendEmailVerificationRateThrottle
from accounts.utils import (generate_strong_6_digit_number,
                            send_verification_email)

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["credentials"],
    request=ResendCodeSerializer,
    responses={
        200: OpenApiResponse(description="Code sent succesfully"),
        500: OpenApiResponse(description="Internal server error"),
    },
)
class ResendCodeView(APIView):
    """
    Resend a fresh email verification code to a user.

    Generates a new 6-digit code (valid 15 minutes), stores it via
    update-or-create so any previous code is replaced, and emails it to the
    user. Already-verified accounts are skipped. To avoid leaking which
    emails exist, the response is the same generic message whether or not the
    account is found or already verified.

    Permissions:
        * AllowAny — open endpoint, no authentication required.

    Required fields:
        * email — the account's email address to resend the code to

    Expected response (200 OK):
        {
            "detail": "If this email exists, a reset code has been sent to verify yourself.",
            "email": <str>   # included only when the account exists
        }

    Errors:
        * 500 Internal Server Error — any unexpected failure:
        {"detail": "An unexpected error occurred while resending the verification code."}
    """

    permission_classes = [AllowAny]
    throttle_classes = [ResendEmailVerificationRateThrottle]

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get("email")
        try:
            user = CustomUser.objects.get(email=email)

            # If already verified, don't resend
            if user.is_verified:
                logger.warning(f"Verified user tried to request new verification code: {email}")
                return Response(
                    {
                        "detail": "If this email exists, a reset code has been sent to verify yourself.",
                        "email": user.email,
                    },
                    status=status.HTTP_200_OK,
                )

            # Generate and save a new code if doesnt exist update otherwise
            verification_code = generate_strong_6_digit_number()

            verification_instance, created = EmailVerification.objects.update_or_create(
                user=user,
                defaults={
                    "code": verification_code,
                    "expires_at": timezone.now() + timedelta(minutes=15),
                },
            )

            # send email
            if not send_verification_email(
                code=str(verification_code),
                email=user.email,
                username=user.username,
            ):
                logger.warning(f"Verification email failed sending for user: {user.username}")

            return Response(
                {
                    "detail": "If this email exists, a reset code has been sent to verify yourself.",
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )

        except ObjectDoesNotExist:
            logger.info(f"Non existing account tried to get email verifiaction code: {email}")
            return Response(
                {
                    "detail": "If this email exists, a reset code has been sent to verify yourself.",
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {
                    "detail": "An unexpected error occurred while resending the verification code.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
