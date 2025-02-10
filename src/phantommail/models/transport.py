from typing import List

from pydantic import BaseModel

from phantommail.models.goods import Goods


class Client(BaseModel):
    """A client of the transport company."""

    name: str
    sender_name: str
    company: str
    address: str
    country: str
    email: str


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
    loading_stops: List[Address]
    unloading_stops: List[Address]
