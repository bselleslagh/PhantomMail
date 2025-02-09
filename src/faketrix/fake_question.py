import random

from faker import Faker


class TransportQuestionGenerator:
    """Generate a fake transport-related question."""

    def __init__(self):
        """Initialize the transport question generator."""
        # Using a single locale for simplicity, you can add more locales if needed.
        self.faker = Faker("en_GB")
        self.question_templates = [
            "What is the scheduled pickup time at {pickup_address}?",
            "When will the goods be delivered to {delivery_address}?",
            "Which route is planned for the transport from {pickup_city} to {delivery_city}?",
            "What are the loading stops for the order leaving from {pickup_city}?",
            "Can you confirm the transport details for the shipment from {pickup_company}?",
        ]

    def generate_question(self) -> dict:
        """Generate a fake transport question using random details.

        Returns:
            dict: Contains the question text and sender information

        """
        template = random.choice(self.question_templates)
        # Generate fake details to populate the question
        pickup_address = self.faker.address()
        delivery_address = self.faker.address()
        pickup_city = self.faker.city()
        delivery_city = self.faker.city()
        pickup_company = self.faker.company()
        sender_name = self.faker.name()

        question = template.format(
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            pickup_city=pickup_city,
            delivery_city=delivery_city,
            pickup_company=pickup_company,
        )

        return {
            "question": question,
            "sender_name": sender_name,
            "formatted_message": f"{question}\n\nBest regards,\n{sender_name}",
        }
