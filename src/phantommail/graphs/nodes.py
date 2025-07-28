import json
import random
from importlib import resources

from google import genai
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from phantommail.fakers.complaint import FakeComplaint
from phantommail.fakers.declaration import DeclarationGenerator
from phantommail.fakers.question import TransportQuestionGenerator
from phantommail.fakers.transport import TransportOrderGenerator
from phantommail.graphs.state import FakeEmailState
from phantommail.helpers.html_to_pdf import create_pdf
from phantommail.logger import setup_logger
from phantommail.models.email import Email, FullEmail
from phantommail.send_email import send

logger = setup_logger(__name__)


class GraphNodes:
    """The nodes for the fake email graph."""

    def __init__(self):
        """Initialize the graph nodes."""
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)

    def email_types(self, state: FakeEmailState, config):
        """Get the email types."""
        types = ["order", "question", "complaint", "declaration"]

        if "email_type" in state and state["email_type"] in types:
            return state["email_type"]

        return random.choice(types)

    async def generate_declaration(self, state: FakeEmailState, config):
        """Generate a fake customs declaration email."""
        declaration_generator = DeclarationGenerator()
        declaration = declaration_generator.generate_declaration()

        html_template = (
            resources.files("phantommail.assets")
            .joinpath("customs_template.html")
            .read_text()
        )

        instruction = SystemMessage(
            content="You are an assistant that generates the HTML version of a customs declaration. You only return raw HTML, no other text."
        )

        prompt = HumanMessage(
            content=f"""Generate the HTML version of the following customs declaration.\n
{declaration}\n\n
Use the following HTML template to generate the HTML version of the customs declaration.\n
{html_template}
        """
        )

        class HTMLTemplate(BaseModel):
            html: str

        llm_with_tools = self.llm.with_structured_output(HTMLTemplate)

        messages = [instruction, prompt]
        response = llm_with_tools.invoke(messages)
        pdf = create_pdf(response.html)
        messages.append(AIMessage(content=response.html))
        messages.append(
            HumanMessage(
                content="Now this document will be added as an attachment to the email."
            )
        )

        return {"messages": messages, "attachments": [pdf]}

    async def generate_question(self, state: FakeEmailState, config):
        """Generate a fake question email."""
        question_generator = TransportQuestionGenerator()
        question = question_generator.generate_question()

        instruction = SystemMessage(
            content="You are an assistant that generates fake emails. The emails are meant for Vectrix Logistcs NV"
        )

        prompt = HumanMessage(
            content=f"""Generate a fake question email based on the following data. Write all details in the body.\n
        {question}
        """
        )

        messages = [instruction, prompt]
        response = self.llm.invoke(messages)
        messages.append(response)

        return {"messages": messages}

    async def generate_complaint(self, state: FakeEmailState, config):
        """Generate a fake complaint email."""
        complaint_generator = FakeComplaint()
        complaint = complaint_generator.generate_complaint()

        instruction = SystemMessage(
            content="You are an assistant that generates fake emails. The emails are meant for Vectrix Logistcs NV"
        )

        prompt = HumanMessage(
            content=f"""Generate a fake complaint email based on the following data. Write all details in the body.\n
        {complaint}
        """
        )
        messages = [instruction, prompt]
        response = self.llm.invoke(messages)
        messages.append(response)

        return {"messages": messages}

    async def generate_order(self, state: FakeEmailState, config):
        """Generate a fake transport order email."""
        transport_order_generator = TransportOrderGenerator()
        transport_order = transport_order_generator.generate().model_dump()

        # Read HTML templates
        email_html = (
            resources.files("phantommail.examples")
            .joinpath("order_2_email.html")
            .read_text()
        )

        pdf_html = (
            resources.files("phantommail.examples")
            .joinpath("order_2_pdf.html")
            .read_text()
        )

        instruction = "You are an assistant that generates fake emails. The emails are meant for VecTrans NV"

        prompt = f"""Generate a fake transport order email based on the following data. Write all details in the body.\n
        Transport details:\n
        {transport_order}

        Create an email body and attachment in the following style:
        <body_html>
        {email_html}
        </body_html>

        <attachment_html>
        {pdf_html}
        </attachment_html>
        """

        client = genai.Client(
            vertexai=True,
            project="vectrix-401014",
            location="global",
        )

        response = await client.aio.models.generate_content(
            model="gemini-2.5-flash",
            contents=[instruction, prompt],
            config={
                "response_mime_type": "application/json",
                "response_schema": Email,
                "temperature": 0,
            },
        )
        response = json.loads(response.text)
        pdf = create_pdf(response["attachment_html"])

        logger.info(f"Response from model: {response}")

        return {
            "attachments": [pdf],
            "email": response["body_html"],
            "subject": response["subject"],
        }

    async def send_email(self, state: FakeEmailState, config):
        """Send an email."""
        email = FullEmail(
            sender=config["configurable"].get("sender"),
            to=state["recipients"],
            attachments=state.get("attachments", []),
            body_html=state["email"],
            subject=state["subject"],
        )

        send(email)

        return {"messages": state["messages"]}
