from datetime import date
from typing import List

from pydantic import BaseModel

from phantommail.models.goods import Goods


class Client(BaseModel):
    """A client of the transport company."""

    name: str
    sender_name: str
    company: str
    vat_number: str
    address: str
    city: str
    postal_code: str
    country: str
    email: str
    phone: str


class Address(BaseModel):
    """An address of the transport company."""

    company: str
    address: str
    country: str


class TransportOrder(BaseModel):
    """A transport order."""

    client: Client
    goods: Goods
    pickup_address: Address
    delivery_address: Address
    intermediate_loading_stops: List[Address]
    intermediate_unloading_stops: List[Address]
    loading_date: date
    unloading_date: date
