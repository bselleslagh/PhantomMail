import pytest
from faker import Faker

from phantommail.fakers.transport import TransportOrderGenerator
from phantommail.models.transport import Address, Client, Goods, TransportOrder


@pytest.fixture
def generator():
    return TransportOrderGenerator()


def test_generate_client(generator):
    client = generator.generate_client()
    assert isinstance(client, Client)
    assert isinstance(client.name, str)
    assert isinstance(client.sender_name, str)
    assert isinstance(client.company, str)
    assert isinstance(client.address, str)
    assert isinstance(client.country, str)
    assert isinstance(client.email, str)
    assert "@" in client.email  # Basic email validation


def test_generate_goods(generator):
    goods = generator.generate_goods()
    assert isinstance(goods, Goods)
    assert isinstance(goods.name, str)
    assert 1 <= goods.quantity <= 100
    assert 350 <= goods.weight <= 1000
    assert 10 <= goods.volume <= 1000
    assert isinstance(goods.description, str)


def test_generate_address(generator):
    faker = Faker()
    address = generator.generate_address(faker)
    assert isinstance(address, Address)
    assert isinstance(address.company, str)
    assert isinstance(address.address, str)
    assert isinstance(address.country, str)


def test_generate_stops(generator):
    faker = Faker()
    stops = generator.generate_stops(3, faker)
    assert len(stops) == 3
    assert all(isinstance(stop, Address) for stop in stops)


def test_generate_transport_order(generator):
    order = generator.generate()
    assert isinstance(order, TransportOrder)
    assert isinstance(order.client, Client)
    assert isinstance(order.goods, Goods)
    assert isinstance(order.pickup_address, Address)
    assert isinstance(order.delivery_address, Address)
    assert isinstance(order.loading_stops, list)
    assert isinstance(order.unloading_stops, list)
    assert all(isinstance(stop, Address) for stop in order.loading_stops)
    assert all(isinstance(stop, Address) for stop in order.unloading_stops)
    assert len(order.loading_stops) <= 3
    assert len(order.unloading_stops) <= 3


def test_different_countries_for_pickup_delivery(generator):
    order = generator.generate()
    # Pickup should be from a random European country
    assert order.pickup_address.country in generator.european_countries
    # Delivery should be in the UK
    assert order.delivery_address.country == "United Kingdom"
