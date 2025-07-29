import csv
import random
from datetime import date, timedelta
from pathlib import Path
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

        # Load customers from CSV
        self.customers = []
        csv_path = Path(__file__).parent.parent / "assets" / "customers.csv"
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.customers = list(reader)

    def generate_client(self) -> Client:
        """Generate a fake client."""
        # Select a random customer from the CSV
        customer = random.choice(self.customers)

        return Client(
            name=customer["company_name"],
            sender_name=self.fake_pickup.name(),  # Generate a random contact person
            company=customer["company_name"],
            vat_number=customer["vat_number"],
            address=customer["address"],
            city=customer["city"],
            postal_code=customer["postal_code"],
            country=customer["country"],
            email=customer["email"],
            phone=customer["phone"],
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

        loading_stops = self.generate_stops(random.randint(0, 1), self.fake_pickup)
        unloading_stops = self.generate_stops(random.randint(0, 1), self.fake_delivery)

        # Generate loading date between tomorrow and 10 days from now
        tomorrow = date.today() + timedelta(days=1)
        loading_date = tomorrow + timedelta(days=random.randint(0, 9))

        # Generate unloading date at least 1 day after loading, up to 5 days later
        unloading_date = loading_date + timedelta(days=random.randint(1, 5))

        return TransportOrder(
            client=client,
            goods=Goods.random(),
            pickup_address=pickup_address,
            delivery_address=delivery_address,
            intermediate_loading_stops=loading_stops,
            intermediate_unloading_stops=unloading_stops,
            loading_date=loading_date,
            unloading_date=unloading_date,
        )
