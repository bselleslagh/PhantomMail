from typing import List

from pydantic import BaseModel


class Email(BaseModel):
    """An email."""

    subject: str
    body_html: str
    attachment_html: str | None = None


class FullEmail(Email):
    """A full email."""

    sender: str
    to: List[str]
    cc: List[str] | None = None
    bcc: List[str] | None = None
    attachments: List[str] | None = None
