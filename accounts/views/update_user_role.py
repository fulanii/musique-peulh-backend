import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
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
        200: OpenApiResponse(UserSerializer, description="User updated successfully"),
        400: OpenApiResponse(description="Invalid data"),
        404: OpenApiResponse(description="User not found"),
    },
)
class UpdateToAdminView(APIView):
    """
    View to update user to admin using their id
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserSerializer

    def patch(self, request):
        data = request.data
        id = data.get("id")

        try:
            instance = CustomUser.objects.get(id=id)

            with transaction.atomic():
                instance.is_staff = True
                instance.is_superuser = True
                instance.save(update_fields=["is_staff", "is_superuser"])

            serialize_data = UserSerializer(instance)

            logger.info(f"User {instance.username} upgraded to admin by {request.user.username}")
            return Response(serialize_data.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise NotFound(detail=f"User with ID '{id}' was not found.")

        except Exception as e:
            logger.error(f"Error occured while upgrading user to admin: {e}")
            return Response(
                {"detail": "An internal server error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
