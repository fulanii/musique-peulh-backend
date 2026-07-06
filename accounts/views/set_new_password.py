import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import CustomUser, PasswordResetCode
from accounts.serializer import PasswordResetSerializer
from accounts.throttles import PasswordResetRateThrottle

logger = logging.getLogger(__name__)


@extend_schema(tags=["credentials"])
class PasswordResetView(APIView):
    """
    Set a new password after verifying the emailed reset code.

    Looks up the user by email and their stored `PasswordResetCode`. If the
    code matches and hasn't expired, the new password is hashed and saved,
    the account is marked verified, and the reset code is deleted (atomically).

    Permissions:
        * AllowAny — open endpoint, no authentication required.

    Throttle:
        * 5/hour (scope "password_reset").

    Required fields:
        * email — the account's email address
        * code — the reset code received by email
        * new_password — the new password to set

    Expected response (200 OK):
        {"detail": "Password reset successful."}

    Errors:
        * 400 Bad Request — {"detail": "Invalid code"} if the code doesn't
          match, {"detail": "Code expired"} if it has expired, or a generic
          failure if no matching account/code exists.
        * 500 Internal Server Error — any unexpected failure:
          {"detail": "An unexpected error occurred reseting password."}
    """

    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRateThrottle]

    def patch(self, request):
        email = request.data["email"]
        code = request.data["code"]
        new_password = request.data["new_password"]

        try:
            user = CustomUser.objects.get(email=email)
            reset_code = PasswordResetCode.objects.get(user=user.id)

            if reset_code.code != int(code):
                return Response({"detail": "Invalid code"}, status=400)

            if reset_code.is_expired:
                return Response({"detail": "Code expired"}, status=400)

            # check if code provided by user match one in password reset db
            with transaction.atomic():
                # Hash and update new password in user db
                user.set_password(raw_password=new_password)
                user.is_verified = True
                user.save()

                reset_code.delete()

            logger.info(f"Password reset successful. {email}")

            return Response({"detail": "Password reset successful."}, status=status.HTTP_200_OK)

        # Handle exceptions
        except ObjectDoesNotExist:
            return Response({"detail": "Something went wrong, password can't be reset."}, status=400)
        except Exception as e:
            return Response(
                {
                    "detail": "An unexpected error occurred reseting password.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
