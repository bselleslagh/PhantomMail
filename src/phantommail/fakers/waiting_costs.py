import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker


class WaitingCostsGenerator:
    """Generate fake waiting cost dispute scenarios."""

    def __init__(self):
        """Initialize the waiting costs generator."""
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

        # Waiting reasons
        self.waiting_reasons = {
            "English": [
                "there was no forklift driver on site",
                "the warehouse was unexpectedly closed",
                "nobody was available to receive the goods",
                "the delivery address was incorrect",
                "access to the delivery point was restricted",
                "the unloading dock was occupied",
            ],
            "Dutch": [
                "er was geen heftruckchauffeur aanwezig",
                "het magazijn was onverwacht gesloten",
                "er was niemand aanwezig om de goederen in ontvangst te nemen",
                "het afleveradres was incorrect",
                "toegang tot het afleveradres was beperkt",
                "het losperron was bezet",
            ],
            "German": [
                "es war kein Staplerfahrer vor Ort",
                "das Lager war unerwartet geschlossen",
                "niemand war verfügbar, um die Ware entgegenzunehmen",
                "die Lieferadresse war falsch",
                "der Zugang zum Lieferort war eingeschränkt",
                "die Entladestelle war besetzt",
            ],
            "Spanish": [
                "no había conductor de carretilla elevadora en el sitio",
                "el almacén estaba inesperadamente cerrado",
                "nadie estaba disponible para recibir la mercancía",
                "la dirección de entrega era incorrecta",
                "el acceso al punto de entrega estaba restringido",
                "el muelle de descarga estaba ocupado",
            ],
            "French": [
                "il n'y avait pas de cariste sur place",
                "l'entrepôt était fermé de manière inattendue",
                "personne n'était disponible pour recevoir les marchandises",
                "l'adresse de livraison était incorrecte",
                "l'accès au point de livraison était restreint",
                "le quai de déchargement était occupé",
            ],
        }

        # Dispute templates
        self.dispute_templates = {
            "English": [
                "I understand that this is a difficult situation. If such cases arise, we need to be informed asap, so that we can work with {destination_company} to find a solution. You cannot send the truck away and bill us for the costs. That's not how it works.",
                "We acknowledge the inconvenience caused to your driver. However, we must dispute these charges as we were not informed of the issue when it occurred. In future, please contact us immediately so we can resolve such situations together.",
                "While we regret the delay experienced by your driver, we cannot accept these waiting charges. Our protocol requires immediate notification of delivery issues to allow us to coordinate with the delivery location.",
            ],
            "Dutch": [
                "Ik begrijp dat dit een moeilijke situatie is. Als dergelijke gevallen zich voordoen, moeten we zo snel mogelijk geïnformeerd worden, zodat we met {destination_company} kunnen samenwerken om een oplossing te vinden. U kunt de vrachtwagen niet wegsturen en ons de kosten in rekening brengen. Zo werkt het niet.",
                "We erkennen het ongemak voor uw chauffeur. We moeten deze kosten echter betwisten omdat we niet op de hoogte zijn gesteld toen het probleem zich voordeed. Neem in de toekomst onmiddellijk contact met ons op zodat we dergelijke situaties samen kunnen oplossen.",
                "Hoewel we de vertraging voor uw chauffeur betreuren, kunnen we deze wachtkosten niet accepteren. Ons protocol vereist onmiddellijke melding van leveringsproblemen zodat we kunnen coördineren met de leveringslocatie.",
            ],
            "German": [
                "Ich verstehe, dass dies eine schwierige Situation ist. Wenn solche Fälle auftreten, müssen wir umgehend informiert werden, damit wir mit {destination_company} eine Lösung finden können. Sie können den LKW nicht wegschicken und uns die Kosten in Rechnung stellen. So funktioniert das nicht.",
                "Wir erkennen die Unannehmlichkeiten für Ihren Fahrer an. Wir müssen diese Gebühren jedoch anfechten, da wir nicht informiert wurden, als das Problem auftrat. Bitte kontaktieren Sie uns in Zukunft sofort, damit wir solche Situationen gemeinsam lösen können.",
                "Obwohl wir die Verzögerung für Ihren Fahrer bedauern, können wir diese Wartegebühren nicht akzeptieren. Unser Protokoll erfordert eine sofortige Benachrichtigung bei Lieferproblemen, damit wir mit dem Lieferort koordinieren können.",
            ],
            "Spanish": [
                "Entiendo que esta es una situación difícil. Si surgen estos casos, necesitamos ser informados lo antes posible para poder trabajar con {destination_company} y encontrar una solución. No pueden enviar el camión y cobrarnos los costos. Así no funciona.",
                "Reconocemos las molestias causadas a su conductor. Sin embargo, debemos disputar estos cargos ya que no fuimos informados del problema cuando ocurrió. En el futuro, contáctenos inmediatamente para resolver estas situaciones juntos.",
                "Aunque lamentamos el retraso experimentado por su conductor, no podemos aceptar estos cargos de espera. Nuestro protocolo requiere notificación inmediata de problemas de entrega para coordinar con el lugar de entrega.",
            ],
            "French": [
                "Je comprends que c'est une situation difficile. Si de tels cas se présentent, nous devons être informés dès que possible afin de travailler avec {destination_company} pour trouver une solution. Vous ne pouvez pas renvoyer le camion et nous facturer les frais. Ce n'est pas ainsi que cela fonctionne.",
                "Nous reconnaissons le désagrément causé à votre chauffeur. Cependant, nous devons contester ces frais car nous n'avons pas été informés du problème lorsqu'il s'est produit. À l'avenir, veuillez nous contacter immédiatement afin que nous puissions résoudre ces situations ensemble.",
                "Bien que nous regrettions le retard subi par votre chauffeur, nous ne pouvons accepter ces frais d'attente. Notre protocole exige une notification immédiate des problèmes de livraison pour nous permettre de coordonner avec le lieu de livraison.",
            ],
        }

        # Closing phrases
        self.closings = {
            "English": [
                "If you have any problems with deliveries in the future, please let us know immediately and we will try to support.",
                "Please ensure immediate communication in future cases to avoid such situations.",
                "We appreciate your understanding and look forward to improved coordination in the future.",
            ],
            "Dutch": [
                "Als u in de toekomst problemen heeft met leveringen, laat het ons dan onmiddellijk weten en we zullen proberen te ondersteunen.",
                "Zorg voor onmiddellijke communicatie in toekomstige gevallen om dergelijke situaties te vermijden.",
                "We waarderen uw begrip en kijken uit naar verbeterde coördinatie in de toekomst.",
            ],
            "German": [
                "Wenn Sie in Zukunft Probleme mit Lieferungen haben, lassen Sie es uns bitte sofort wissen und wir werden versuchen zu unterstützen.",
                "Bitte stellen Sie in zukünftigen Fällen eine sofortige Kommunikation sicher, um solche Situationen zu vermeiden.",
                "Wir schätzen Ihr Verständnis und freuen uns auf eine verbesserte Koordination in der Zukunft.",
            ],
            "Spanish": [
                "Si tiene algún problema con las entregas en el futuro, háganoslo saber de inmediato e intentaremos apoyar.",
                "Asegure una comunicación inmediata en casos futuros para evitar estas situaciones.",
                "Apreciamos su comprensión y esperamos una mejor coordinación en el futuro.",
            ],
            "French": [
                "Si vous avez des problèmes avec les livraisons à l'avenir, veuillez nous en informer immédiatement et nous essaierons de vous aider.",
                "Veuillez assurer une communication immédiate dans les cas futurs pour éviter de telles situations.",
                "Nous apprécions votre compréhension et attendons avec impatience une meilleure coordination à l'avenir.",
            ],
        }

    def generate_waiting_costs_scenario(self) -> dict:
        """Generate a fake waiting costs dispute scenario.

        Returns:
            dict: Contains the waiting costs scenario and dispute response

        """
        # Select a random customer
        customer = random.choice(self.customers)

        # Get language info based on customer country
        locale, language = self.languages.get(customer["country"], ("en_GB", "English"))
        faker = Faker(locale)

        # Generate scenario details
        delivery_city = faker.city()
        destination_company = faker.company()
        delivery_date = date.today() - timedelta(days=random.randint(1, 7))

        # Generate reference numbers
        order_ref = f"{random.randint(20250000, 20259999)}/{random.randint(1, 99):02d}"
        delivery_ref = str(random.randint(50000000, 59999999))
        internal_ref = str(random.randint(700000, 799999))
        tracking_ref = f"VTR{random.randint(100000, 999999)}"

        # Generate waiting details
        waiting_hours = random.randint(3, 8)
        cost_per_hour = random.randint(50, 75)
        total_cost = waiting_hours * cost_per_hour

        # Select waiting reason
        waiting_reason = random.choice(
            self.waiting_reasons.get(language, self.waiting_reasons["English"])
        )

        # Generate sender details for the dispute
        sender_name = faker.name()
        titles = {
            "English": [
                "Logistics Manager",
                "Transport Manager",
                "Supply Chain Manager",
            ],
            "Dutch": ["Logistiek Manager", "Transport Manager", "Supply Chain Manager"],
            "German": ["Leiter Logistik", "Verkehrsleiter", "Supply Chain Manager"],
            "Spanish": [
                "Gerente de Logística",
                "Gerente de Transporte",
                "Gerente de Cadena de Suministro",
            ],
            "French": [
                "Responsable Logistique",
                "Responsable Transport",
                "Responsable Supply Chain",
            ],
        }
        sender_title = random.choice(titles.get(language, titles["English"]))

        # Select dispute message
        dispute_template = random.choice(self.dispute_templates[language])
        dispute_message = dispute_template.format(
            destination_company=destination_company
        )

        # Select closing
        closing_message = random.choice(self.closings[language])

        # Build signature
        if language == "English":
            formal_closing = "Regards"
        elif language == "Dutch":
            formal_closing = "Met vriendelijke groet"
        elif language == "German":
            formal_closing = "Mit freundlichen Grüßen"
        elif language == "Spanish":
            formal_closing = "Saludos cordiales"
        elif language == "French":
            formal_closing = "Cordialement"
        else:
            formal_closing = "Best regards"

        signature = f"""{formal_closing}

{sender_name}
{sender_title}

{customer["company_name"]}
{customer["address"]}
{customer["postal_code"]} {customer["city"]}
{customer["country"]}

Phone: {customer["phone"]}
Email: {customer["email"]}"""

        # Format the complete dispute message
        formatted_message = f"""{dispute_message}

{closing_message}

{signature}"""

        return {
            "scenario": {
                "delivery_city": delivery_city,
                "destination_company": destination_company,
                "delivery_date": delivery_date.strftime("%d/%m/%Y"),
                "order_ref": order_ref,
                "delivery_ref": delivery_ref,
                "internal_ref": internal_ref,
                "tracking_ref": tracking_ref,
                "waiting_reason": waiting_reason,
                "waiting_hours": waiting_hours,
                "total_cost": total_cost,
            },
            "dispute_message": dispute_message,
            "closing_message": closing_message,
            "sender_name": sender_name,
            "sender_title": sender_title,
            "company": customer["company_name"],
            "language": language,
            "signature": signature,
            "formatted_message": formatted_message,
        }
