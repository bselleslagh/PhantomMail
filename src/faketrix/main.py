import os

from dotenv import load_dotenv

from faketrix.graphs.graph import graph
from faketrix.logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)


def main():
    """Mail function that sends an email to the recipient."""
    recipient = input("Please enter the recipient's email address: ")
    config = {"configurable": {"sender": os.environ["SENDER_EMAIL"]}}
    response = graph.invoke({"recipients": [recipient]}, config=config)
    return response


if __name__ == "__main__":
    main()
