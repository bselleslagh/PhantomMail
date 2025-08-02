from typing import List

from pydantic import BaseModel, Field


class Email(BaseModel):
    """An email."""

    subject: str = Field(..., description="The subject line of the email")
    body_html: str = Field(..., description="The HTML content of the email body")
    attachment_html: str | None = Field(
        None,
        description="Optional HTML content for email attachments, do not include if no data is provided",
    )


class FullEmail(Email):
    """A full email."""

    sender: str = Field(..., description="The email address of the sender")
    to: List[str] = Field(..., description="List of recipient email addresses")
    cc: List[str] | None = Field(
        None, description="List of CC (carbon copy) recipient email addresses"
    )
    bcc: List[str] | None = Field(
        None, description="List of BCC (blind carbon copy) recipient email addresses"
    )
    attachments: List[str] | None = Field(
        None, description="List of file paths or names for email attachments"
    )
