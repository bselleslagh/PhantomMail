import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker


class RandomPromotionalGenerator:
    """Generate random promotional emails for transport services."""

    def __init__(self):
        """Initialize the random promotional generator."""
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

        # Promotional themes by language
        self.promo_themes = {
            "English": [
                {
                    "title": "New Express Routes Now Available!",
                    "content": "We're excited to announce new express delivery routes to major European cities. Get your goods delivered 30% faster!",
                    "benefit": "30% faster delivery times",
                    "cta": "Contact us to learn more about our express routes",
                },
                {
                    "title": "Special Discount on International Transport",
                    "content": "For a limited time, enjoy {discount}% off on all international shipments over 1000km.",
                    "benefit": "{discount}% discount on long-distance transport",
                    "cta": "Book your transport today and save",
                },
                {
                    "title": "Introducing Our Advanced Tracking System",
                    "content": "Track your shipments in real-time with our new GPS-enabled tracking platform. Know exactly where your goods are, 24/7.",
                    "benefit": "Real-time shipment tracking",
                    "cta": "Request a demo of our tracking system",
                },
                {
                    "title": "Fleet Expansion - More Capacity Available",
                    "content": "We've added 50 new trucks to our fleet! More capacity means faster booking and better availability for your transport needs.",
                    "benefit": "Increased transport capacity",
                    "cta": "Reserve your spot now",
                },
                {
                    "title": "Green Transport Initiative",
                    "content": "Join us in reducing carbon emissions! Our new eco-friendly fleet offers the same reliability with 40% less environmental impact.",
                    "benefit": "40% lower carbon emissions",
                    "cta": "Learn about our sustainability program",
                },
            ],
            "Dutch": [
                {
                    "title": "Nieuwe Express Routes Nu Beschikbaar!",
                    "content": "We zijn verheugd om nieuwe express leveringsroutes naar grote Europese steden aan te kondigen. Krijg uw goederen 30% sneller geleverd!",
                    "benefit": "30% snellere levertijden",
                    "cta": "Neem contact op voor meer informatie over onze express routes",
                },
                {
                    "title": "Speciale Korting op Internationaal Transport",
                    "content": "Voor een beperkte tijd, geniet van {discount}% korting op alle internationale zendingen boven 1000km.",
                    "benefit": "{discount}% korting op lange afstand transport",
                    "cta": "Boek vandaag uw transport en bespaar",
                },
                {
                    "title": "Introductie van Ons Geavanceerde Tracking Systeem",
                    "content": "Volg uw zendingen in real-time met ons nieuwe GPS-tracking platform. Weet precies waar uw goederen zijn, 24/7.",
                    "benefit": "Real-time zending tracking",
                    "cta": "Vraag een demo aan van ons tracking systeem",
                },
            ],
            "German": [
                {
                    "title": "Neue Express-Routen jetzt verfügbar!",
                    "content": "Wir freuen uns, neue Express-Lieferrouten zu großen europäischen Städten anzukündigen. Ihre Waren werden 30% schneller geliefert!",
                    "benefit": "30% schnellere Lieferzeiten",
                    "cta": "Kontaktieren Sie uns für mehr Informationen",
                },
                {
                    "title": "Sonderrabatt auf internationale Transporte",
                    "content": "Für begrenzte Zeit erhalten Sie {discount}% Rabatt auf alle internationalen Sendungen über 1000km.",
                    "benefit": "{discount}% Rabatt auf Ferntransporte",
                    "cta": "Buchen Sie heute und sparen Sie",
                },
                {
                    "title": "Grüne Transport-Initiative",
                    "content": "Reduzieren Sie mit uns CO2-Emissionen! Unsere neue umweltfreundliche Flotte bietet die gleiche Zuverlässigkeit mit 40% weniger Umweltbelastung.",
                    "benefit": "40% weniger CO2-Emissionen",
                    "cta": "Erfahren Sie mehr über unser Nachhaltigkeitsprogramm",
                },
            ],
            "Spanish": [
                {
                    "title": "¡Nuevas Rutas Express Disponibles!",
                    "content": "Nos complace anunciar nuevas rutas de entrega express a las principales ciudades europeas. ¡Sus mercancías se entregan un 30% más rápido!",
                    "benefit": "30% tiempos de entrega más rápidos",
                    "cta": "Contáctenos para más información",
                },
                {
                    "title": "Descuento Especial en Transporte Internacional",
                    "content": "Por tiempo limitado, disfrute de un {discount}% de descuento en todos los envíos internacionales de más de 1000km.",
                    "benefit": "{discount}% de descuento en transporte de larga distancia",
                    "cta": "Reserve su transporte hoy y ahorre",
                },
            ],
            "French": [
                {
                    "title": "Nouvelles Routes Express Disponibles!",
                    "content": "Nous sommes ravis d'annoncer de nouvelles routes de livraison express vers les grandes villes européennes. Vos marchandises livrées 30% plus rapidement!",
                    "benefit": "30% de temps de livraison en moins",
                    "cta": "Contactez-nous pour en savoir plus",
                },
                {
                    "title": "Réduction Spéciale sur le Transport International",
                    "content": "Pour une durée limitée, bénéficiez de {discount}% de réduction sur tous les envois internationaux de plus de 1000km.",
                    "benefit": "{discount}% de réduction sur le transport longue distance",
                    "cta": "Réservez votre transport aujourd'hui et économisez",
                },
            ],
        }

        # Titles by language
        self.titles = {
            "English": [
                "Sales Manager",
                "Business Development Manager",
                "Marketing Manager",
            ],
            "Dutch": [
                "Sales Manager",
                "Business Development Manager",
                "Marketing Manager",
            ],
            "German": [
                "Vertriebsleiter",
                "Geschäftsentwicklungsleiter",
                "Marketing Manager",
            ],
            "Spanish": [
                "Gerente de Ventas",
                "Gerente de Desarrollo de Negocios",
                "Gerente de Marketing",
            ],
            "French": [
                "Responsable Commercial",
                "Responsable Développement",
                "Responsable Marketing",
            ],
        }

        # Closing phrases
        self.closings = {
            "English": ["Best regards", "Kind regards", "Sincerely"],
            "Dutch": ["Met vriendelijke groet", "Vriendelijke groeten", "Hoogachtend"],
            "German": ["Mit freundlichen Grüßen", "Freundliche Grüße", "Beste Grüße"],
            "Spanish": ["Saludos cordiales", "Atentamente", "Un cordial saludo"],
            "French": ["Cordialement", "Bien cordialement", "Sincères salutations"],
        }

    def generate_promotional_email(self) -> dict:
        """Generate a random promotional email.

        Returns:
            dict: Contains the promotional email content and sender information

        """
        # Select a random customer
        customer = random.choice(self.customers)

        # Get language info based on customer country
        locale, language = self.languages.get(customer["country"], ("en_GB", "English"))
        faker = Faker(locale)

        # Select promotional theme
        promo_themes = self.promo_themes.get(language, self.promo_themes["English"])
        promo = random.choice(promo_themes)

        # Generate discount if needed
        discount = random.randint(10, 30)
        promo_content = promo["content"].format(discount=discount)
        promo_benefit = promo["benefit"].format(discount=discount)

        # Generate validity period
        start_date = date.today()
        end_date = start_date + timedelta(days=random.randint(14, 30))

        # Generate sender details
        sender_name = faker.name()
        title = random.choice(self.titles.get(language, self.titles["English"]))

        # Select closing
        closing = random.choice(self.closings.get(language, self.closings["English"]))

        # Build signature
        signature = f"""{closing}

{sender_name}
{title}

{customer["company_name"]}
{customer["address"]}
{customer["postal_code"]} {customer["city"]}
{customer["country"]}

Phone: {customer["phone"]}
Email: {customer["email"]}
Web: www.{customer["company_name"].lower().replace(" ", "").replace(".", "")}.com"""

        # Format validity text by language
        validity_text = {
            "English": f"Valid from {start_date.strftime('%d/%m/%Y')} to {end_date.strftime('%d/%m/%Y')}",
            "Dutch": f"Geldig van {start_date.strftime('%d/%m/%Y')} tot {end_date.strftime('%d/%m/%Y')}",
            "German": f"Gültig vom {start_date.strftime('%d.%m.%Y')} bis {end_date.strftime('%d.%m.%Y')}",
            "Spanish": f"Válido desde {start_date.strftime('%d/%m/%Y')} hasta {end_date.strftime('%d/%m/%Y')}",
            "French": f"Valable du {start_date.strftime('%d/%m/%Y')} au {end_date.strftime('%d/%m/%Y')}",
        }

        return {
            "promo_title": promo["title"],
            "promo_content": promo_content,
            "promo_benefit": promo_benefit,
            "promo_cta": promo["cta"],
            "validity": validity_text.get(language, validity_text["English"]),
            "sender_name": sender_name,
            "sender_title": title,
            "company": customer["company_name"],
            "language": language,
            "signature": signature,
            "closing": closing,
        }
