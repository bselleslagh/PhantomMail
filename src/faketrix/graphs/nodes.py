import random

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from faketrix.fake_transport import TransportOrderGenerator
from faketrix.graphs.state import FakeEmailState
from faketrix.models.email import Email, FullEmail
from faketrix.send_email import send_email


class GraphNodes:
    """The nodes for the fake email graph."""

    def __init__(self):
        """Initialize the graph nodes."""
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001", temperature=0.5)

    def generate_fake_data(self, state: FakeEmailState, config):
        """Generate a fake transport order."""
        transport_order_generator = TransportOrderGenerator()
        transport_order = transport_order_generator.generate().model_dump()
        return {"email_attributes": transport_order}

    def generate_email(self, state: FakeEmailState, config):
        """Generate a fake transport order email."""
        writing_style = [
            "fast and with spelling mistakes",
            "detailed and polite",
            "in the oringal language of the sender",
        ]

        instruction = SystemMessage(
            content="You are an assistant that generates fake emails. The emails are meant for Vectrix Logistcs NV"
        )

        prompt = HumanMessage(
            content=f"""Generate a fake transport order email based on the following data. Your writing style should be {random.choice(writing_style)}. Write all details in the body.\n
        Transport details:\n
        {state["email_attributes"]}
        """
        )
        messages = [instruction, prompt]
        response = self.llm.invoke(messages)
        messages.append(response)

        return {"messages": messages}

    def body_to_html(self, state: FakeEmailState, config):
        """Convert the body of the email to HTML."""
        llm_with_tools = self.llm.bind_tools([Email])
        messages = state["messages"]
        writing_style = [
            "fast and with spelling mistakes",
            "detailed and polite",
            "in the oringal language of the sender",
        ]
        prompt = HumanMessage(
            content=f"Convert the draft email to HTML and return it as a function call. Make the email look messy and unprofessional. Your writing style should be {random.choice(writing_style)}."
        )
        messages.append(prompt)
        response = llm_with_tools.invoke(messages)

        return {"messages": [prompt, response]}

    def send_email(self, state: FakeEmailState, config):
        """Send an email."""
        response = state["messages"][-1]
        email = FullEmail(
            sender=config["configurable"].get("sender"),
            to=state["recipients"],
            **response.tool_calls[0]["args"],
        )
        response = send_email(email)

        return {"messages": state["messages"]}
