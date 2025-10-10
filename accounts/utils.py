import secrets


def generate_strong_6_digit_number():
    """Generates a cryptographically strong random 6-digit number as a string."""

    random_int = secrets.randbelow(1_000_000)

    return int(f"{random_int:06d}")


# TODO: implement this using my domain (no-reply@musiquepeulh.com) and resend
def send_verification_email():
    """Send verification code to user email"""
