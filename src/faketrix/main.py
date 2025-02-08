import os

import resend
from dotenv import load_dotenv

from faketrix.fake_transport import TransportOrderGenerator
from faketrix.logger import setup_logger

logger = setup_logger(__name__)

transport_order_generator = TransportOrderGenerator()


def send_email(recipient_email: str) -> None:
    """Send an email to the recipient with the given subject and body.

    Args:
        recipient_email (str): The email address of the recipient.

    Returns:
        str: A message indicating that the email was sent successfully.

    """
    load_dotenv()
    resend.api_key = os.environ["RESEND_API_KEY"]

    params: resend.Emails.SendParams = {
        "from": os.environ["SENDER_EMAIL"],
        "to": [recipient_email],
        "subject": "hello world",
        "html": "<strong>it works!</strong>",
    }

    try:
        email = resend.Emails.send(params)
        logger.info(f"Email sent successfully! ID: {email}")
    except Exception as e:
        logger.error(f"Error sending email: {e}")


def main():
    """Mail function that sends an email to the recipient."""
    recipient = input("Please enter the recipient's email address: ")
    send_email(recipient)


if __name__ == "__main__":
    main()
