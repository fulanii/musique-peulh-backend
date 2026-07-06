import logging

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import CustomUser
from accounts.serializer import UserSerializer

logger = logging.getLogger(__name__)


@extend_schema(tags=["user"])
class GetUsersView(APIView):
    """
    List all users in the system (admin only).

    Returns every user account, serialized with UserSerializer.

    Permissions:
        * IsAuthenticated + IsAdminUser (JWT) — requires a valid access token
          for a staff/admin user.

    Required fields:
        * None — this is a GET request with no body.

    Expected response (200 OK):
        A list of serialized users (UserSerializer):
        [
            {
                "id": <int>,
                "email": <str>,
                "username": <str>,
                "is_staff": <bool>,
                "is_superuser": <bool>,
                "is_verified": <bool>,
                ...
            },
            ...
        ]

    Errors:
        * 401 Unauthorized — missing or invalid access token.
        * 403 Forbidden — authenticated but not an admin user.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        queryset = CustomUser.objects.all()

        serialize_data = UserSerializer(queryset, many=True)

        logger.info(f"All users profile data requested by {request.user.username}")

        return Response(serialize_data.data, status=status.HTTP_200_OK)
