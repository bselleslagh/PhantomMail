from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class FakeEmailState(TypedDict):
    """The attributes for passing to LangGraph."""

    recipients: Annotated[list[str], "The recipients of the email"]
    email_attributes: Annotated[dict, "The attributes of the email"]
    email: Annotated[dict, "The subject and body of the email"]
    messages: Annotated[list, add_messages]
    attachments: Annotated[list[str], "The attachments of the email"]
    email_type: Annotated[str, "The type of email to generate"]
    subject: Annotated[str, "The subject of the email"]
