import logging

from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from songs.serializers import YtDataResponseSerializer, YtDownloadSerializer
from songs.tasks import download_and_upload
from songs.utils import get_yt_data

logger = logging.getLogger(__name__)


@extend_schema(tags=["songs-admin"])
class YoutubeDownload(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    throttle_classes = []

    # ------------------- For displaying video data (title, duration, channel name)
    @extend_schema(parameters=[OpenApiParameter("url", str, OpenApiParameter.QUERY, required=True)], responses={200: YtDataResponseSerializer})
    def get(self, request):
        """
        Preview a YouTube video's metadata before downloading (admin only).

        Fetches metadata for the given video URL (title, duration, channel,
        thumbnail) without downloading the media, so an admin can review or
        pre-fill the song details before committing the download.

        Permissions:
            * IsAuthenticated + IsAdminUser (JWT) — requires a valid access
            token for a staff/admin user.

        Required fields:
            * url (query param) — the YouTube video URL to preview.

        Expected response (200 OK):
            Video metadata (YtDataResponseSerializer):
            {
                "title": <str>,
                "duration": <int>,          # seconds
                "duration_string": <str>,   # e.g. "3:45"
                "channel": <str>,
                "thumbnail": <str>          # URL
            }

        Errors:
            * 400 Bad Request — missing url query param:
            {"detail": "url is required."}
            * 401 Unauthorized — missing or invalid access token.
            * 403 Forbidden — authenticated but not an admin user.
            * 500 Internal Server Error — metadata extraction failed
            (invalid/removed/private video):
            {"detail": "Something went wrong while extracting youtube video data."}
        """
        url = request.query_params.get("url")

        if not url:
            return Response(
                {"detail": "url is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = get_yt_data(url=url)

        if data is None:
            logger.error(f"Something went wrong while extracting youtube video data.")
            return Response({"detail": "Something went wrong while extracting youtube video data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        info_serializer = YtDataResponseSerializer(data)

        logger.info("Successfully downloaded video data.")
        return Response(info_serializer.data, status=status.HTTP_200_OK)


    # ------------------- For downloading video
    # @extend_schema(request=YtDownloadSerializer, responses={202: OpenApiResponse(description="Processing, will automatically upload.")})
    # def post(self, request):
    #     """

    #     """

    #     user = request.user

    #     yt_serializer = YtDownloadSerializer(data=request.data)
    #     yt_serializer.is_valid(raise_exception=True)
    #     validated_data = yt_serializer.validated_data

    #     url = validated_data.get("url")

    #     # submit background task to download and upload
    #     download_and_upload(url=url)

    #     # send response processing
    #     return Response(
    #         {"detail": "Processing, will automatically upload."},
    #         status=status.HTTP_202_ACCEPTED
    #     )
