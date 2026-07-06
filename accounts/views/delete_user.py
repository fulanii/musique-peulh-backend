from django.db import transaction
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import CustomUser
from accounts.serializer import GetUserIdSerializer, UserSerializer


@extend_schema(
    tags=["user"],
    request=GetUserIdSerializer,
    responses={
        200: OpenApiResponse(UserSerializer, description="User deleted successfully"),
        400: OpenApiResponse(description="Invalid id data"),
        404: OpenApiResponse(description="User not found"),
    },
)
class DeleteUserView(APIView):
    """
    Delete a user by ID.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        id = kwargs["id"]

        try:
            instance = CustomUser.objects.get(id=id)
            with transaction.atomic():
                instance.delete()
            return Response({"success": True, "deleted_user_id": id}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
