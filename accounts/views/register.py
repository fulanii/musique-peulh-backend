import logging

from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import CustomUser, EmailVerification
from accounts.serializer import RegisterSerializer
from accounts.utils import (generate_strong_6_digit_number,
                            send_verification_email)

logger = logging.getLogger(__name__)


@extend_schema(tags=["credentials"])
class RegisterUserView(CreateAPIView):
    """
    Register a new user and send a 6-digit email verification code.

    Creates the account, generates an `EmailVerification` code, and emails it
    to the user. The account is created even if the verification email fails to
    send (the failure is only logged).

    Permissions:
        * AllowAny — open endpoint, no authentication required.

    Required fields:
        * email — user's email address (must be unique)
        * username — desired username (must be unique)
        * password — account password

    Expected response (201 Created):
        {
            "registration_success": true,
            "message": "Account created successfully.",
            "id": <int>,
            "email": <str>,
            "username": <str>
        }

    Errors:
        * 500 Bad Request — invalid/missing fields (serializer validation), or the verification code could not be created: {"error": "Something went wrong."}
    """

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                self.perform_create(serializer)

                verification_code = generate_strong_6_digit_number()
                code_data = EmailVerification.objects.create(user=serializer.instance, code=verification_code)

        except Exception as e:
            logger.error(f"Something went wrong: {e}")
            return Response(
                {"error": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if not send_verification_email(
            code=str(verification_code),
            email=serializer.data["email"],
            username=serializer.data["username"],
        ):
            logger.warning(f"Verification email failed sending for user: {request.user.username}")

        # Custom response data
        custom_data = {
            "registration_success": True,
            "message": "Account created successfully.",
            "id": serializer.instance.pk,  # created object's ID
            "email": serializer.data["email"],
            "username": serializer.data["username"],
        }

        logger.info(f"user '{custom_data['username']}' registration successful")

        headers = self.get_success_headers(serializer.data)
        return Response(custom_data, status=status.HTTP_201_CREATED, headers=headers)
