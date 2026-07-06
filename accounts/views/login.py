import logging

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import CustomUser
from accounts.serializer import LoginSerializer
from accounts.throttles import LoginRateThrottle

logger = logging.getLogger(__name__)


@extend_schema(tags=["credentials"])
class LoginUserView(APIView):
    """
    Authenticate a user and issue JWT access/refresh tokens.

    Accepts either an email or a username via a single `identifier` field
    (an "@" in the value is treated as an email, otherwise a username).
    On success, returns the token pair plus basic user data.

    Permissions:
        * AllowAny — open endpoint, no authentication required.

    Required fields:
        * identifier — the user's email address or username
        * password — account password

    Expected response (200 OK):
        {
            "refresh": <str>,
            "access": <str>,
            "user_data": {
                "id": <int>,
                "email": <str>,
                "username": <str>,
                "is_staff": <bool>,
                "is_superuser": <bool>,
                "is_verified": <bool>
            }
        }

    Errors:
        * 400 Bad Request — missing fields, unknown email/username, or
          invalid credentials (serializer validation).
    """

    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer_class = LoginSerializer(data=request.data, context={"request": request})
        serializer_class.is_valid(raise_exception=True)

        user = serializer_class.validated_data["user"]

        full_user_data = CustomUser.objects.filter(email=user.email).values()

        user_data = full_user_data.first()

        user_data_returned = {
            "id": user_data["id"],
            "email": user_data["email"],
            "username": user_data["username"],
            "is_staff": user_data["is_staff"],
            "is_superuser": user_data["is_superuser"],
            "is_verified": user_data["is_verified"],
        }

        # TODO: Return refresh token in http only cookie
        # issue JWT tokens
        refresh = RefreshToken.for_user(user)

        logger.info(f"user '{user_data['username']}' login successful")

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_data": user_data_returned,
            },
            status=status.HTTP_200_OK,
        )
