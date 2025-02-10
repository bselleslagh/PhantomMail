import random
from typing import List

from faker import Faker

from phantommail.models.goods import Goods
from phantommail.models.transport import Address, Client, TransportOrder


class TransportOrderGenerator:
    """Generate a fake transport order."""

    def __init__(self):
        """Initialize the transport order generator."""
        self.european_countries = {
            "Germany": "de_DE",
            "France": "fr_FR",
            "Spain": "es_ES",
            "Belgium": "nl_BE",
            "Poland": "pl_PL",
            "Austria": "de_AT",
            "Switzerland": "de_CH",
            "United Kingdom": "en_GB",
            "Portugal": "pt_PT",
        }
        # Initialize Faker instances
        self.fake_pickup = Faker(random.choice(list(self.european_countries.values())))
        self.fake_delivery = Faker("en_GB")

    def generate_client(self) -> Client:
        """Generate a fake client."""
        return Client(
            name=self.fake_pickup.company(),
            sender_name=self.fake_pickup.name(),
            company=self.fake_pickup.company(),
            address=self.fake_pickup.address(),
            country=self.fake_pickup.current_country(),
            email=self.fake_pickup.ascii_company_email(),
        )

    def generate_address(self, faker_instance: Faker) -> Address:
        """Generate a fake address."""
        return Address(
            company=faker_instance.company(),
            address=faker_instance.address(),
            country=faker_instance.current_country(),
        )

    def generate_stops(self, count: int, faker_instance: Faker) -> List[Address]:
        """Generate a list of fake addresses."""
        return [self.generate_address(faker_instance) for _ in range(count)]

    def generate(self) -> TransportOrder:
        """Generate a fake transport order."""
        client = self.generate_client()
        pickup_address = self.generate_address(self.fake_pickup)
        delivery_address = self.generate_address(self.fake_delivery)

        loading_stops = self.generate_stops(random.randint(0, 3), self.fake_pickup)
        unloading_stops = self.generate_stops(random.randint(0, 3), self.fake_delivery)

        return TransportOrder(
            client=client,
            goods=Goods.random(),
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            loading_stops=loading_stops,
            unloading_stops=unloading_stops,
        )
