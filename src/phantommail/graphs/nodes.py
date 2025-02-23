import random
from importlib import resources

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

from phantommail.fakers.complaint import FakeComplaint
from phantommail.fakers.declaration import DeclarationGenerator
from phantommail.fakers.question import TransportQuestionGenerator
from phantommail.fakers.transport import TransportOrderGenerator
from phantommail.graphs.state import FakeEmailState
from phantommail.helpers.html_to_pdf import create_pdf
from phantommail.models.email import Email, FullEmail
from phantommail.send_email import send


class GraphNodes:
    """The nodes for the fake email graph."""

    def __init__(self):
        """Initialize the graph nodes."""
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0.5)

    def email_types(self, state: FakeEmailState, config):
        """Get the email types."""
        types = ["order", "question", "complaint", "declaration"]

        if state["email_type"] in types:
            return state["email_type"]

        return random.choice(types)

    def generate_declaration(self, state: FakeEmailState, config):
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

    def generate_question(self, state: FakeEmailState, config):
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

    def generate_complaint(self, state: FakeEmailState, config):
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

    def generate_order(self, state: FakeEmailState, config):
        """Generate a fake transport order email."""
        transport_order_generator = TransportOrderGenerator()
        transport_order = transport_order_generator.generate().model_dump()

        instruction = SystemMessage(
            content="You are an assistant that generates fake emails. The emails are meant for Vectrix Logistcs NV"
        )

        prompt = HumanMessage(
            content=f"""Generate a fake transport order email based on the following data. Write all details in the body.\n
        Transport details:\n
        {transport_order}
        """
        )
        messages = [instruction, prompt]
        response = self.llm.invoke(messages)
        messages.append(response)

        return {"messages": messages}

    def body_to_html(self, state: FakeEmailState, config):
        """Convert the body of the email to HTML."""
        llm_with_tools = self.llm.with_structured_output(Email)
        messages = state["messages"]
        writing_style = [
            "fast and with spelling mistakes",
            "detailed and polite",
            "in the oringal language of the sender",
        ]
        prompt = HumanMessage(
            content=f"""Convert the draft email to HTML and return it as a function call.\n
Your writing style should be {random.choice(writing_style)}.
You can also add some history, context and custom HTML formatting to the email to make it look more realistic.
            """
        )
        messages.append(prompt)
        response = llm_with_tools.invoke(messages)

        messages = [prompt, AIMessage(content=response.body)]

        return {"messages": messages, "email": response}

    def send_email(self, state: FakeEmailState, config):
        """Send an email."""
        response = state["email"]
        email = FullEmail(
            sender=config["configurable"].get("sender"),
            to=state["recipients"],
            attachments=state.get("attachments", []),
            **response.model_dump(),
        )

        response = send(email)

        return {"messages": state["messages"]}
