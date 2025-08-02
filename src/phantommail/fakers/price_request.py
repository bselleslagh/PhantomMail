import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker


class PriceRequestGenerator:
    """Generate a fake transport price request."""

    def __init__(self):
        """Initialize the price request generator."""
        self.languages = {
            "Netherlands": ("nl_NL", "Dutch"),
            "United Kingdom": ("en_GB", "English"),
            "Sweden": ("en_GB", "English"),
            "Belgium": ("nl_BE", "Dutch"),
            "Spain": ("es_ES", "Spanish"),
            "Germany": ("de_DE", "German"),
            "Poland": ("en_GB", "English"),
            "Italy": ("en_GB", "English"),
            "France": ("fr_FR", "French"),
            "Austria": ("de_AT", "German"),
            "Switzerland": ("de_CH", "German"),
            "Portugal": ("pt_PT", "English"),
        }

        # Load customers from CSV
        self.customers = []
        csv_path = Path(__file__).parent.parent / "assets" / "customers.csv"
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.customers = list(reader)

        # Transport titles by language
        self.titles = {
            "Dutch": [
                "Transport Manager",
                "Logistiek Coördinator",
                "Inkoop Manager Transport",
            ],
            "English": [
                "Transport Manager",
                "Logistics Coordinator",
                "Procurement Manager",
            ],
            "Spanish": [
                "Gerente de Transporte",
                "Coordinador Logístico",
                "Jefe de Compras",
            ],
            "German": [
                "Transport Manager",
                "Logistikkoordinator",
                "Einkaufsleiter Transport",
            ],
            "French": [
                "Responsable Transport",
                "Coordinateur Logistique",
                "Responsable Achats",
            ],
        }

        # Price negotiation templates
        self.price_templates = {
            "Dutch": [
                "Kunnen we akkoord gaan met {proposed_price}€? Ik heb momenteel {budget_price}€ voor deze bestemming.",
                "Voor de route {origin} - {destination} kan ik maximaal {budget_price}€ bieden. Is dit bespreekbaar?",
                "We hebben een budget van {budget_price}€ voor dit transport. Kunnen jullie een betere prijs aanbieden?",
            ],
            "English": [
                "Could we agree on {proposed_price}€? I actually have {budget_price}€ for this destination.",
                "For the route {origin} - {destination}, I can offer maximum {budget_price}€. Is this negotiable?",
                "We have a budget of {budget_price}€ for this transport. Can you offer a better price?",
            ],
            "Spanish": [
                "¿Podríamos acordar {proposed_price}€? En realidad tengo {budget_price}€ para este destino.",
                "Para la ruta {origin} - {destination}, puedo ofrecer máximo {budget_price}€. ¿Es negociable?",
                "Tenemos un presupuesto de {budget_price}€ para este transporte. ¿Pueden ofrecer un mejor precio?",
            ],
            "German": [
                "Könnten wir uns auf {proposed_price}€ einigen? Ich habe tatsächlich {budget_price}€ für dieses Ziel.",
                "Für die Route {origin} - {destination} kann ich maximal {budget_price}€ anbieten. Ist das verhandelbar?",
                "Wir haben ein Budget von {budget_price}€ für diesen Transport. Können Sie einen besseren Preis anbieten?",
            ],
            "French": [
                "Pourrions-nous nous mettre d'accord sur {proposed_price}€? J'ai en fait {budget_price}€ pour cette destination.",
                "Pour le trajet {origin} - {destination}, je peux offrir maximum {budget_price}€. Est-ce négociable?",
                "Nous avons un budget de {budget_price}€ pour ce transport. Pouvez-vous offrir un meilleur prix?",
            ],
        }

        # Closing phrases by language
        self.closings = {
            "Dutch": ["Met vriendelijke groet", "Vriendelijke groeten", "Hoogachtend"],
            "English": ["Best regards", "Kind regards", "Regards"],
            "Spanish": ["Saludos cordiales", "Atentamente", "Un saludo"],
            "German": ["Mit freundlichen Grüßen", "Freundliche Grüße", "Beste Grüße"],
            "French": ["Cordialement", "Bien cordialement", "Meilleures salutations"],
        }

    def generate_price_request(self) -> dict:
        """Generate a fake price request with customer details from CSV.

        Returns:
            dict: Contains the price request details and sender information

        """
        # Select a random customer
        customer = random.choice(self.customers)

        # Get language info based on customer country
        locale, language = self.languages.get(customer["country"], ("en_GB", "English"))
        faker = Faker(locale)

        # Generate sender details
        sender_name = faker.name()
        title = random.choice(self.titles[language])

        # Generate route details
        origin_city = faker.city()
        destination_city = faker.city()

        # Generate price details
        base_price = random.randint(1500, 4000)
        proposed_price = base_price + random.randint(100, 500)
        budget_price = base_price - random.randint(100, 400)

        # Generate transport date
        transport_date = date.today() + timedelta(days=random.randint(7, 30))

        # Select and format price message
        template = random.choice(self.price_templates[language])
        price_message = template.format(
            proposed_price=proposed_price,
            budget_price=budget_price,
            origin=origin_city,
            destination=destination_city,
        )

        # Select closing
        closing = random.choice(self.closings[language])

        # Build signature block
        if language == "German":
            signature = f"""{closing}

i.A. {sender_name}

{title}

Standort {customer["city"]}


Telefon {customer["phone"]}
{customer["email"]}
www.{customer["company_name"].lower().replace(" ", "").replace(".", "")}.com

{customer["company_name"]}
{customer["address"]}  |  {customer["postal_code"]} {customer["city"]}

USt.-Ident. {customer["vat_number"]}"""
        else:
            signature = f"""{closing}

{sender_name}
{title}

{customer["company_name"]}
{customer["address"]}
{customer["postal_code"]} {customer["city"]}
{customer["country"]}

Phone: {customer["phone"]}
Email: {customer["email"]}
VAT: {customer["vat_number"]}"""

        return {
            "price_message": price_message,
            "sender_name": sender_name,
            "sender_title": title,
            "company": customer["company_name"],
            "language": language,
            "origin": origin_city,
            "destination": destination_city,
            "transport_date": transport_date.strftime("%d/%m/%Y"),
            "proposed_price": proposed_price,
            "budget_price": budget_price,
            "signature": signature,
            "formatted_message": f"{price_message}\n\n{signature}",
        }
