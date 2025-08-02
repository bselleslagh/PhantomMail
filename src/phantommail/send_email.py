"""Email sending functionality using the Resend API."""

import base64
import os

import resend

from phantommail.logger import setup_logger
from phantommail.models.email import FullEmail

logger = setup_logger(__name__)


def send(email: FullEmail) -> str:
    """Send an email to the recipient with the given subject and body.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
        recipient_email (str): The email address of the recipient.

    Returns:
        str: A message indicating that the email was sent successfully.

    """
    logger.info(f"Sending email to {email.to} with subject: {email.subject}")
    resend.api_key = os.environ["RESEND_API_KEY"]
    params: resend.Emails.SendParams = {
        "from": email.sender,
        "to": email.to,
        "subject": email.subject,
        "html": email.body_html,
        "cc": email.cc,
        "bcc": email.bcc,
    }
    if len(email.attachments) > 0:
        params["attachments"] = [
            {
                "content": list(base64.b64decode(attachment.encode("utf-8"))),
                "filename": f"attachment_{i}.pdf",
            }
            for i, attachment in enumerate(email.attachments)
        ]
    try:
        email = resend.Emails.send(params)
        logger.info("Email sent successfully! ")
        return "Email sent successfully!"
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return f"Error sending email: {e}"
