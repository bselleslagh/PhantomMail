import random
from importlib import resources

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
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
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.5)

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
        pdf = await create_pdf(response.html)
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

        logger.info(f"Generated transport order: {transport_order}")

        # Randomly select an order template (1-5)
        order_number = random.randint(1, 5)
        logger.info(f"Selected order template: order_{order_number}")

        # Read HTML templates
        email_html = (
            resources.files("phantommail.examples")
            .joinpath(f"order_{order_number}_email.html")
            .read_text()
        )

        # Check if PDF template exists for this order
        if order_number == 1:
            # Order 1 doesn't have a PDF template
            pdf_html = "no attachment"
        else:
            pdf_html = (
                resources.files("phantommail.examples")
                .joinpath(f"order_{order_number}_pdf.html")
                .read_text()
            )

        # Format transport details for use in prompts
        transport_details = f"""
        ## Sender details:
        - Company name: {transport_order["client"]["company"]}
        - Contact person: {transport_order["client"]["sender_name"]}
        - VAT number: {transport_order["client"]["vat_number"]}
        - Address: {transport_order["client"]["address"]}
        - City: {transport_order["client"]["city"]}
        - Postal code: {transport_order["client"]["postal_code"]}
        - Country: {transport_order["client"]["country"]}
        - Email: {transport_order["client"]["email"]}
        - Phone: {transport_order["client"]["phone"]}

        ## Goods details:
        - Description: {transport_order["goods"]}

        ## Transport dates:
        - Loading date: {transport_order["loading_date"]}
        - Unloading date: {transport_order["unloading_date"]}

        ## Pickup address:
        - Company: {transport_order["pickup_address"]["company"]}
        - Address: {transport_order["pickup_address"]["address"]}
        - Country: {transport_order["pickup_address"]["country"]}

        ## Delivery address:
        - Company: {transport_order["delivery_address"]["company"]}
        - Address: {transport_order["delivery_address"]["address"]}
        - Country: {transport_order["delivery_address"]["country"]}

        ## Intermediate Loading stops: {len(transport_order["intermediate_loading_stops"])}
        {chr(10).join([f"        - {stop['company']}, {stop['address']}, {stop['country']}" for stop in transport_order["intermediate_loading_stops"]])}

        ## Intermediate Unloading stops: {len(transport_order["intermediate_unloading_stops"])}
        {chr(10).join([f"        - {stop['company']}, {stop['address']}, {stop['country']}" for stop in transport_order["intermediate_unloading_stops"]])}
        """

        if pdf_html == "no attachment":
            prompt = f"""Generate a fake transport order email based on the following data. 
        
        IMPORTANT: Replace ALL references in the HTML template with the actual data provided below:
        - Replace all company names, addresses, contact details with the sender's information
        - Replace order numbers, dates, and transport details with realistic values
        - Replace any placeholder text with appropriate content based on the transport order
        - Ensure the email appears to come from the sender company listed below
        
        Transport details:
        {transport_details}

        Create an email body in the following style:
        <body_html>
        {email_html}
        </body_html>

        <attachment_html>
        no attachment
        </attachment_html>
        """
        else:
            prompt = f"""Generate a fake transport order email based on the following data.
        
        IMPORTANT: Replace ALL references in BOTH the email HTML and attachment HTML templates with the actual data:
        - Replace all company names, addresses, contact details with the sender's information
        - Replace order numbers, dates, and transport details with realistic values
        - Replace any placeholder text with appropriate content based on the transport order
        - Ensure both the email and PDF attachment appear to come from the sender company
        - Make sure the attachment contains detailed transport information matching the email
        
        Transport details:
        {transport_details}

        Create an email body and attachment in the following style:
        <body_html>
        {email_html}
        </body_html>

        <attachment_html>
        {pdf_html}
        </attachment_html>
        """

        llm = ChatVertexAI(
            model="gemini-2.5-pro",
            temperature=0,
        )

        llm_with_tools = llm.with_structured_output(Email)

        response = await llm_with_tools.ainvoke(
            [
                HumanMessage(content=prompt),
            ]
        )

        response = response.model_dump()

        # Check if we need to create a PDF attachment based on order number
        if order_number != 1:
            pdf = await create_pdf(response["attachment_html"])
            attachments = [pdf]
        else:
            attachments = []

        logger.info(f"Response from model: {response}")

        return {
            "attachments": attachments,
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
