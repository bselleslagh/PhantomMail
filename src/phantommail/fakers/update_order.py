import csv
import random
from pathlib import Path

from faker import Faker


class UpdateOrderGenerator:
    """Generate fake update order questions."""

    def __init__(self):
        """Initialize the update order generator."""
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

        # Update questions by language
        self.question_templates = {
            "English": [
                "could you please send us the trailer and truck number?",
                "can you confirm the estimated arrival time?",
                "what is the current status of this transport?",
                "has the truck already departed?",
                "can you provide the driver's contact information?",
                "please confirm the exact loading/unloading times.",
            ],
            "Dutch": [
                "kunt u ons de trailer- en vrachtwagennummer sturen?",
                "kunt u de verwachte aankomsttijd bevestigen?",
                "wat is de huidige status van dit transport?",
                "is de vrachtwagen al vertrokken?",
                "kunt u de contactgegevens van de chauffeur verstrekken?",
                "bevestig alstublieft de exacte laad-/lostijden.",
            ],
            "German": [
                "könnten Sie uns bitte die Anhänger- und LKW-Nummer senden?",
                "können Sie die voraussichtliche Ankunftszeit bestätigen?",
                "was ist der aktuelle Status dieses Transports?",
                "ist der LKW bereits abgefahren?",
                "können Sie die Kontaktdaten des Fahrers mitteilen?",
                "bitte bestätigen Sie die genauen Lade-/Entladezeiten.",
            ],
            "Spanish": [
                "¿podría enviarnos el número de remolque y camión?",
                "¿puede confirmar la hora estimada de llegada?",
                "¿cuál es el estado actual de este transporte?",
                "¿el camión ya ha salido?",
                "¿puede proporcionar la información de contacto del conductor?",
                "por favor confirme los horarios exactos de carga/descarga.",
            ],
            "French": [
                "pourriez-vous nous envoyer le numéro de remorque et de camion?",
                "pouvez-vous confirmer l'heure d'arrivée estimée?",
                "quel est le statut actuel de ce transport?",
                "le camion est-il déjà parti?",
                "pouvez-vous fournir les coordonnées du chauffeur?",
                "veuillez confirmer les heures exactes de chargement/déchargement.",
            ],
        }

        # Greetings by language
        self.greetings = {
            "English": ["Hello", "Good morning", "Good afternoon"],
            "Dutch": ["Hallo", "Goedemorgen", "Goedemiddag"],
            "German": ["Hallo", "Guten Morgen", "Guten Tag"],
            "Spanish": ["Hola", "Buenos días", "Buenas tardes"],
            "French": ["Bonjour", "Bonjour", "Bonjour"],
        }

        # Titles by language
        self.titles = {
            "English": [
                "Transport Coordinator",
                "Logistics Assistant",
                "Operations Assistant",
            ],
            "Dutch": [
                "Transport Coördinator",
                "Logistiek Assistent",
                "Operationeel Assistent",
            ],
            "German": [
                "Transportkoordinator",
                "Logistikassistent",
                "Betriebsassistent",
            ],
            "Spanish": [
                "Coordinador de Transporte",
                "Asistente Logístico",
                "Asistente de Operaciones",
            ],
            "French": [
                "Coordinateur Transport",
                "Assistant Logistique",
                "Assistant Opérations",
            ],
        }

        # Closing signatures by language
        self.closing_signatures = {
            "English": "Kind regards",
            "Dutch": "Met vriendelijke groet",
            "German": "Mit freundlichen Grüßen",
            "Spanish": "Saludos cordiales",
            "French": "Cordialement",
        }

    def generate_update_order_question(self) -> dict:
        """Generate a fake update order question.

        Returns:
            dict: Contains the update order question and sender information

        """
        # Select a random customer
        customer = random.choice(self.customers)

        # Get language info based on customer country
        locale, language = self.languages.get(customer["country"], ("en_GB", "English"))
        faker = Faker(locale)

        # Generate sender details
        sender_name = faker.name()
        title = random.choice(self.titles[language])

        # Generate reference numbers
        order_ref = f"{random.randint(20250000, 20259999)}/{random.randint(1, 99):02d}"
        tracking_ref = f"VTR{random.randint(100000, 999999)}"

        # Select greeting and question
        greeting = random.choice(self.greetings[language])
        question = random.choice(self.question_templates[language])

        # Get closing signature
        closing = self.closing_signatures[language]

        # Build multi-language closing
        if language == "German":
            # German style with multi-language closings
            multi_closing = f"{closing} | Kind regards | Z poważaniem"
            abbreviation = "i. A."
        else:
            multi_closing = closing
            abbreviation = ""

        # Build signature
        if abbreviation:
            name_line = f"{abbreviation} {sender_name}"
        else:
            name_line = sender_name

        signature = f"""{multi_closing}

{name_line}

Telefon: {customer["phone"]}
E-Mail: {customer["email"]}

{customer["company_name"]} | {customer["address"]} | {customer["postal_code"]} {customer["city"]} | {customer["country"]}"""

        # Add additional company info for German companies
        if language == "German":
            signature += f"""

USt.-Id Nr.: {customer["vat_number"]}"""

        # Format the complete message
        formatted_message = f"""{greeting},

{question}

{signature}"""

        return {
            "greeting": greeting,
            "question": question,
            "sender_name": sender_name,
            "sender_title": title,
            "company": customer["company_name"],
            "language": language,
            "order_ref": order_ref,
            "tracking_ref": tracking_ref,
            "signature": signature,
            "formatted_message": formatted_message,
        }
