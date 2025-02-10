import random
from datetime import datetime

from faker import Faker

from phantommail.models.customs_document import (
    CustomsDeclaration,
    ItemDetail,
    Party,
    TaxLine,
    TransportInfo,
)
from phantommail.models.goods import Goods


class DeclarationGenerator:
    """Generate a fake customs declaration."""

    def __init__(self):
        """Initialize the declaration generator."""
        self.faker = Faker()

    def _generate_party(self) -> Party:
        """Generate a fake party with name, address and EORI number."""
        return Party(
            name=self.faker.company(),
            address=self.faker.address(),
            eori_number=f"GB{self.faker.numerify('#########')}",
        )

    def _generate_transport_info(self) -> TransportInfo:
        """Generate fake transport information."""
        return TransportInfo(
            arrival_transport=self.faker.license_plate(),
            border_transport=self.faker.license_plate(),
            transport_mode=random.randint(1, 9),
            place_of_loading=self.faker.city(),
        )

    def _generate_item_detail(self, goods: Goods, item_number: int) -> ItemDetail:
        """Generate a fake item detail based on a goods object."""
        return ItemDetail(
            item_number=item_number,
            packages=goods.quantity,
            shipping_marks=self.faker.bothify(text="??-####"),
            commodity_code=self.faker.numerify(text="########"),
            description_of_goods=goods.description,
            gross_mass_kg=goods.weight,
            net_mass_kg=goods.weight * 0.95,  # Assuming packaging is 5% of weight
        )

    def _generate_tax_line(self) -> TaxLine:
        """Generate a fake tax line."""
        tax_base = round(random.uniform(100, 10000), 2)
        tax_rate = random.choice([0, 5, 10, 15, 20])
        total_tax = round(tax_base * (tax_rate / 100), 2)

        return TaxLine(
            tax_type=random.choice(["A00", "B00"]),  # A00 = Customs duties, B00 = VAT
            tax_base=tax_base,
            tax_rate=tax_rate,
            total_tax_assessed=total_tax,
            amount_payable=total_tax,
        )

    def generate_declaration(self) -> CustomsDeclaration:
        """Generate a fake customs declaration."""
        # Generate a random goods item
        goods = Goods.random()

        # Generate tax lines
        tax_lines = [self._generate_tax_line() for _ in range(random.randint(1, 3))]

        return CustomsDeclaration(
            mrn=f"GB{self.faker.numerify('#' * 16)}",
            declaration_type=random.choice(["IM", "EX", "CO"]),
            reference_number=self.faker.bothify(text="??####"),
            forms_count=1,
            items_count=1,
            total_packages=goods.quantity,
            # Parties
            exporter=self._generate_party(),
            importer=self._generate_party(),
            declarant=self._generate_party(),
            representative=self._generate_party(),
            buyer=self._generate_party(),
            # Transport details
            transport_info=self._generate_transport_info(),
            # Items
            items=[self._generate_item_detail(goods, 1)],
            # Valuation & taxes
            invoice_currency=random.choice(["GBP", "EUR", "USD"]),
            invoice_value=round(random.uniform(1000, 100000), 2),
            tax_lines=tax_lines,
            # Acceptance & signature
            acceptance_date_time=datetime.now().isoformat(),
            declaration_status="ACCEPTED",
            place_and_date=f"{self.faker.city()}, {self.faker.date()}",
        )
