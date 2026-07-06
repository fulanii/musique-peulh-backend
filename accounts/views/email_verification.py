import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser, EmailVerification
from accounts.serializer import EmailVerificationSerializer
from accounts.throttles import EmailVerificationRateThrottle

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["credentials"],
    request=EmailVerificationSerializer,
    responses={
        200: OpenApiResponse(description="Email verified succesfully"),
        400: OpenApiResponse(description="Invalid email"),
        500: OpenApiResponse(description="An unexpected error occurred"),
    },
)
class EmailVerificationView(APIView):
    """
    Verify a user's account by matching the emailed verification code.

    Looks up the user by email and their stored `EmailVerification` code.
    If the code matches and hasn't expired, the account is marked verified
    and the code is deleted (atomically). Already-verified accounts return
    success without re-processing.

    Permissions:
        * AllowAny — open endpoint, no authentication required.

    Required fields:
        * email — the email the code was sent to
        * code — the verification code received by email

    Expected response (200 OK):
        {"detail": "Email verified."}

    Errors:
        * 400 Bad Request — {"error": "Invalid code"} if the code doesn't
          match, or {"error": "Code expired"} if it has expired.
        * 404 Not Found — no account exists for the given email:
          {"detail": "Something went wrong. Try again."}
        * 500 Internal Server Error — any unexpected failure:
          {"detail": "An unexpected error occurred."}
    """

    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]
    throttle_classes = [EmailVerificationRateThrottle]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            email = data.get("email")
            entered_code = data.get("code")

            user = CustomUser.objects.get(email=email)
            code_data = EmailVerification.objects.get(user=user.id)

            if user.is_verified:
                return Response(
                    {"detail": "Email verified."},
                    status=status.HTTP_200_OK,
                )

            if code_data.code != int(entered_code):
                return Response({"detail": "Invalid code"}, status=400)

            if code_data.is_expired:
                return Response({"detail": "Code expired"}, status=400)

            with transaction.atomic():
                user.is_verified = True
                user.save()
                code_data.delete()

            logger.info(f"Account verification succesful: {email}")

            return Response(
                {"detail": "Email verified."},
                status=status.HTTP_200_OK,
            )

        except ObjectDoesNotExist:
            logger.info(f"Non existing account tried to verify: {email}")
            raise NotFound(detail="Something went wrong. Email can't be verified.")

        except Exception as e:
            logger.error(f"Error while verifiying account: {e}")
            return Response(
                {
                    "detail": "An unexpected error occurred.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
