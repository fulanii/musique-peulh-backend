import os
import resend
from resend.exceptions import ResendError
import secrets
from dotenv import load_dotenv

# load .env file
load_dotenv()


def generate_strong_6_digit_number():
    """Generates a cryptographically strong random 6-digit number as a string."""

    random_int = secrets.randbelow(1_000_000)

    return int(f"{random_int:06d}")


EMAIL_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verification Code</title>
    <style type="text/css">
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            margin: 0;
            padding: 0;
            background-color: #f6f6f6;
            -webkit-text-size-adjust: 100%;
            -ms-text-size-adjust: 100%;
        }
        table {
            border-collapse: collapse;
            mso-table-lspace: 0pt;
            mso-table-rspace: 0pt;
        }
        td {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            font-size: 16px;
            line-height: 24px;
        }
        a {
            color: #E2B736; /* Primary link color, matching gradient start */
            text-decoration: none;
        }
        /* Mobile responsiveness */
        @media only screen and (max-width: 600px) {
            .container {
                width: 100% !important;
            }
            .code-box {
                font-size: 32px !important;
                padding: 20px 0 !important;
            }
        }
    </style>
</head>
<body style="background-color: #f6f6f6;">

    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f6f6f6;">
        <tr>
            <td align="center" style="padding: 40px 0;">

                <table class="container" border="0" cellpadding="0" cellspacing="0" width="600" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                    
                    <tr>
                        <td style="padding: 30px 40px 20px 40px;">
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span style="
                                    font-size: 24px; 
                                    font-weight: bold; 
                                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                                    /* CUSTOM GRADIENT STYLING */
                                    background-image: linear-gradient(135deg, rgb(226, 183, 54) 0%, rgb(230, 115, 77) 100%);
                                    -webkit-background-clip: text;
                                    -webkit-text-fill-color: transparent;
                                    background-clip: text;
                                    color: rgb(226, 183, 54); /* Fallback color for clients that don't support text clipping */
                                ">
                                    MusiquePeulh
                                </span>
                            </div>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 0 40px;">
                            <hr style="border: 0; border-top: 1px solid #eeeeee; margin: 0;">
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 30px 40px 40px 40px; color: #333333;">
                            
                            <p style="margin: 0 0 20px 0; font-size: 16px; line-height: 24px;">
                                Heyy **[username]**,
                            </p>

                            <p style="margin: 0 0 30px 0; font-size: 16px; line-height: 24px;">
                                Use the code below to verify your email.
                            </p>

                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 30px; border-radius: 4px; border: 1px solid #dddddd; background-color: #f9f9f9;">
                                <tr>
                                    <td align="center" class="code-box" style="padding: 30px 0; font-size: 40px; font-weight: bold; color: #333333; letter-spacing: 5px;">
                                        **[code_here]**
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <tr>
                        <td style="padding: 20px 40px; font-size: 12px; line-height: 18px; color: #999999; background-color: #f6f6f6; border-bottom-left-radius: 8px; border-bottom-right-radius: 8px;">
                            Delivered by MusiquePeulh.
                            <br>
                            <i>Please do not reply to this email.</i>
                        </td>
                    </tr>

                </table>
                </td>
        </tr>
    </table>
    </body>
</html>

"""


def send_verification_email(code: str, email: str, username: str) -> bool:
    """
    Send verification code to user email
    returns True if sucessful False otherwise
    """

    try:
        formaed_html = EMAIL_HTML_TEMPLATE.replace("**[username]**", username)
        formaed_html = formaed_html.replace("**[code_here]**", code)

        resend.api_key = os.getenv("RESEND_API_KEY")

        params: resend.Emails.SendParams = {
            "from": "MusiquePeulh <email-verification@musiquepeulh.com>",
            "to": [f"{email}"],
            "subject": "MusiquePeulh Email Verification: Here's the 6-digit verification code you requested",
            "html": formaed_html,
        }

        email = resend.Emails.send(params)

        return True

    except ResendError:
        return False
