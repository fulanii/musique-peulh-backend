import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import CustomUser
from accounts.serializer import GetUserIdSerializer, UserSerializer

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["user"],
    request=GetUserIdSerializer,  # 👈 this tells Spectacular that we expect JSON body like UserSerializer
    responses={
        200: OpenApiResponse(UserSerializer, description="User found"),
        400: OpenApiResponse(description="Invalid data"),
        404: OpenApiResponse(description="User not found"),
    },
)
class GetUserView(APIView):
    """
    Retrieve a single user's profile by ID.

    Looks up the user by the given `id`. Access is restricted: a user may only
    fetch their own profile unless they are a superuser, who may fetch anyone.

    Permissions:
        * IsAuthenticated (JWT) — a valid access token is required.

    Required fields:
        * id — the ID of the user to retrieve

    Expected response (200 OK):
        Serialized user (UserSerializer):
        {
            "id": <int>,
            "email": <str>,
            "username": <str>,
            "is_staff": <bool>,
            "is_superuser": <bool>,
            "is_verified": <bool>,
            ...
        }

    Errors:
        * 403 Forbidden — requesting another user's profile without superuser
          rights: {"detail": "You do not have permission to view this user."}
        * 404 Not Found — no user exists for the given id.
        * 500 Internal Server Error — any unexpected failure:
          {"detail": "An internal server error occurred."}
    """

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        user_id = data.get("id")

        try:
            instance = CustomUser.objects.get(id=user_id)

            # Allow only if user is admin OR requesting their own profile
            if not request.user.is_superuser and request.user.id != instance.id:
                raise PermissionDenied("You do not have permission to view this user.")

            serialize_data = UserSerializer(instance)

            logger.info(f"User profile data requested by {request.user.username}")
            return Response(serialize_data.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise NotFound(detail=f"User with ID '{user_id}' was not found.")

        except Exception as e:
            logger.error(f"Error occured while getting user data: {e}")
            return Response(
                {"detail": "An internal server error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
