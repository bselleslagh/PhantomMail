import random

from faker import Faker


class FakeComplaint:
    """Generate a fake transport complaint."""

    def __init__(self):
        """Initialize the fake complaint generator."""
        self.faker = Faker("en_GB")
        self.complaint_templates = [
            "I am writing to express my deep dissatisfaction with the delivery service to {delivery_address}. The package was supposed to arrive on {expected_date} but it's still not here.",
            "I want to file a formal complaint about the handling of my shipment from {pickup_address}. The delivery person was extremely rude and damaged my package.",
            "This is unacceptable! My delivery to {delivery_address} was scheduled for {expected_date} but arrived completely damaged.",
            "I am furious about the state of my package delivered to {delivery_address}. The contents were damaged and the box was crushed.",
            "Your service is terrible! My package from {pickup_address} has been delayed for days with no explanation or updates.",
        ]

    def generate_complaint(self) -> dict:
        """Generate a fake transport complaint using random details.

        Returns:
            dict: Contains the complaint text and sender information

        """
        template = random.choice(self.complaint_templates)
        pickup_address = self.faker.address()
        delivery_address = self.faker.address()
        expected_date = self.faker.date_this_month()
        sender_name = self.faker.name()

        complaint = template.format(
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            expected_date=expected_date,
        )

        return {
            "complaint": complaint,
            "sender_name": sender_name,
            "formatted_message": f"{complaint}\n\nRegards,\n{sender_name}",
        }
