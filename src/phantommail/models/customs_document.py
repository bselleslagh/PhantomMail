from typing import List, Optional

from pydantic import BaseModel, Field


class Party(BaseModel):
    """Represents a party such as Exporter, Importer, Declarant, or Buyer."""

    name: str
    address: Optional[str] = None
    eori_number: Optional[str] = None


class TransportInfo(BaseModel):
    """Holds transport‐related information extracted from the form."""

    arrival_transport: Optional[str] = None
    border_transport: Optional[str] = None
    transport_mode: Optional[int] = None
    place_of_loading: Optional[str] = None


class ItemDetail(BaseModel):
    """Represents an individual line item on the customs document."""

    item_number: int
    packages: Optional[int] = None
    shipping_marks: Optional[str] = None
    commodity_code: Optional[str] = None
    description_of_goods: Optional[str] = None
    gross_mass_kg: Optional[float] = None
    net_mass_kg: Optional[float] = None
    # Add further fields like “National additional codes,” “Quota,” etc. as needed.


class TaxLine(BaseModel):
    """Represents a specific tax or duty assessment line."""

    tax_type: str  # e.g. A00 = Customs duties, B00 = VAT
    tax_base: float
    tax_rate: float
    total_tax_assessed: float
    amount_payable: float


class CustomsDeclaration(BaseModel):
    """Top-level model encapsulating the entire declaration."""

    # Basic document info
    mrn: str = Field(..., description="Movement Reference Number")
    declaration_type: str = Field(..., description="E.g., IM D, EX, etc.")
    reference_number: Optional[str] = None
    forms_count: Optional[int] = None
    items_count: Optional[int] = None
    total_packages: Optional[int] = None

    # Parties
    exporter: Optional[Party] = None
    importer: Optional[Party] = None
    declarant: Optional[Party] = None
    representative: Optional[Party] = None
    buyer: Optional[Party] = None

    # Transport details
    transport_info: Optional[TransportInfo] = None

    # Item(s) details
    items: List[ItemDetail] = Field(default_factory=list)

    # Valuation & taxes
    invoice_currency: Optional[str] = None
    invoice_value: Optional[float] = None
    tax_lines: List[TaxLine] = Field(default_factory=list)

    # Acceptance & signature
    acceptance_date_time: Optional[str] = None
    declaration_status: Optional[str] = None
    place_and_date: Optional[str] = None
