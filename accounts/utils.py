import os
import secrets

from brevo import Brevo
from brevo.core.api_error import ApiError
from brevo.transactional_emails import SendTransacEmailRequestSender, SendTransacEmailRequestToItem
from django.conf import settings
from dotenv import load_dotenv


def generate_strong_6_digit_number():
    """Generates a cryptographically strong random 6-digit number as a string."""

    random_int = secrets.randbelow(1_000_000)

    return int(f"{random_int:06d}")


def send_verification_email(code: str, email: str, username: str) -> bool:
    """
    Send verification code to user email
    returns True if sucessful False otherwise
    """

    try:
        # client = Brevo(api_key=settings.BREVO_API_KEY)

        # result = client.transactional_emails.send_transac_email(
        #     template_id=3,
        #     params={"USERNAME": username, "CODE": code},
        #     to=[
        #         SendTransacEmailRequestToItem(
        #             email=email,
        #         )
        #     ],
        # )

        # print("Email sent. Message ID:", result.message_id)

        return True

    except ApiError as e:
        return False


def send_password_reset_code_email(code: str, email: str, username: str) -> bool:
    """
    Send password reset verification code to user email
    returns True if sucessful False otherwise
    """

    try:
        # client = Brevo(api_key=settings.BREVO_API_KEY)

        # result = client.transactional_emails.send_transac_email(
        #     template_id=4,
        #     params={"USERNAME": username, "CODE": code},
        #     to=[
        #         SendTransacEmailRequestToItem(
        #             email=email,
        #         )
        #     ],
        # )

        # print("Email sent. Message ID:", result.message_id)

        return True

    except ApiError as e:
        return False
