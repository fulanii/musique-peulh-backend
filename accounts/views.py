from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import NotFound
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction


from .models import CustomUser
from .serializer import (
    RegisterSerializer,
    LoginSerializer,
    VerificationSerializer,
    UserSerializer,
)
from .utils import generate_strong_6_digit_number


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

        verification_code = generate_strong_6_digit_number()
        serializer.instance.verification_code = verification_code
        serializer.instance.save()

        # TODO: Send Verification code email, Update success msg: Account created successfully, verification email sent!

        # Custom response data
        custom_data = {
            "registration_success": True,
            "message": "Account created successfully",
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

        # issue JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user_data": user_data_returned,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["credentials"])
class Verification(APIView):
    """
    View to verify users by checking user verification code

    * email: user email they received code to
    * code: code receive to email
    """

    serializer_class = VerificationSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get("email")
        code = data.get("code")

        user = CustomUser.objects.get(email=email)

        if not user:
            return Response({"error": "User not found"}, status=404)

        if user.verification_code != code:
            return Response({"error": "Invalid code"}, status=400)

        # TODO: Add code_expires_at
        # if user.code_expires_at < timezone.now():
        #     return Response({"error": "Code expired"}, status=400)
        # user.code_expires_at = None

        user.is_verified = True
        user.verification_code = None
        user.save()

        return Response(
            {"detail": "Email verified. You can now log in."},
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["credentials"])
class GetUser(APIView):
    """
    View to get user using id
    """

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, id):

        try:
            instance = CustomUser.objects.get(id=id)

            serialize_data = UserSerializer(instance)

            return Response(serialize_data.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise NotFound(detail=f"User with ID '{id}' was not found.")

        except Exception as e:
            return Response(
                {"detail": "An internal server error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(tags=["credentials"])
class GetUsers(APIView):
    """
    View to get all users
    """

    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        queryset = CustomUser.objects.all()

        serialize_data = UserSerializer(queryset, many=True)

        return Response(serialize_data.data, status=status.HTTP_200_OK)


@extend_schema(tags=["credentials"])
class UpdateToAdmin(APIView):
    """
    View to update user to admin using their id
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, id):
        try:
            instance = CustomUser.objects.get(id=id)

            with transaction.atomic():
                instance.is_staff = True
                instance.is_superuser = True
                instance.save(update_fields=["is_staff", "is_superuser"])

            serialize_data = UserSerializer(instance)

            return Response(serialize_data.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            raise NotFound(detail=f"User with ID '{id}' was not found.")

        except Exception as e:
            return Response(
                {"detail": "An internal server error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# @extend_schema(tags=["credentials"])
class PasswordReset:  # TODO: Finish reset password
    """
    View to reset users password in the system using

    * email: to recieve code
    """


# TODO: Add delete user functionality
# @extend_schema(tags=["credentials"])
class DeleteUser:  # TODO: Finish delete user
    """
    View to deleter user in the system using

    * id or email or username
    """
