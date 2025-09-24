from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


from .models import CustomUser
from .serializer import RegisterSerializer, LoginSerializer


@extend_schema(tags=["credentials"])
class RegisterUser(CreateAPIView):
    """
    View to register users in the system using

    * email
    * username
    * password
    """

    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Custom response data
        custom_data = {
            "registration_success": True,
            "message": "Account created successfully!",
            "id": serializer.instance.pk,  # created object's ID
            "email": serializer.data["email"],
            "username": serializer.data["username"],
        }

        headers = self.get_success_headers(serializer.data)
        return Response(custom_data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=["credentials"])
class LoginUser(APIView):
    """
    View to log users in the system using

    * email
    * password
    """

    serializer_class = LoginSerializer()

    def post(self, request):

        serializer_class = LoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer_class.is_valid(raise_exception=True)

        user = serializer_class.validated_data["user"]

        # issue JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


# {
#   "email": "yassine@yassinecodes.dev",
#   "username": "yassine",
#   "password": "password"
# }
