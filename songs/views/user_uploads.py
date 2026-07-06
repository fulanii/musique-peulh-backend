from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from songs.models import Song
from songs.serializers import SongSerializer
from songs.throttles import UserUploadsRateThrottle


@extend_schema(tags=["songs-admin"])
class UploadedByUserSongsView(ListAPIView):
    """
    List all songs uploaded by a specific user (admin only).

    Filters songs by the `uploaded_by` username provided in the URL path.

    Permissions:
        * IsAuthenticated + IsAdminUser (JWT) — requires a valid access token
        for a staff/admin user.

    Throttle:
        * 60/min (scope "user_uploads").

    Required fields:
        * uploaded_by (URL path) — the username whose uploads to list.

    Expected response (200 OK):
        A list of serialized songs (SongSerializer) uploaded by that user;
        an empty list if the user has no uploads.

    Errors:
        * 401 Unauthorized — missing or invalid access token.
        * 403 Forbidden — authenticated but not an admin user.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = [UserUploadsRateThrottle]

    serializer_class = SongSerializer

    def get_queryset(self):
        uploaded_by = self.kwargs["uploaded_by"]
        return Song.objects.filter(uploaded_by=uploaded_by)
