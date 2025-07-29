import pytest
from faker import Faker
from datetime import date, timedelta

from phantommail.fakers.transport import TransportOrderGenerator
from phantommail.models.transport import Address, Client, TransportOrder
from phantommail.models.goods import Goods


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
    goods = Goods.random()
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
    assert isinstance(order.intermediate_loading_stops, list)
    assert isinstance(order.intermediate_unloading_stops, list)
    assert all(isinstance(stop, Address) for stop in order.intermediate_loading_stops)
    assert all(isinstance(stop, Address) for stop in order.intermediate_unloading_stops)
    assert len(order.intermediate_loading_stops) <= 1
    assert len(order.intermediate_unloading_stops) <= 1
    
    # Test the new date fields
    assert isinstance(order.loading_date, date)
    assert isinstance(order.unloading_date, date)
    
    # Loading date should be between tomorrow and 10 days from now
    tomorrow = date.today() + timedelta(days=1)
    ten_days_later = date.today() + timedelta(days=10)
    assert tomorrow <= order.loading_date <= ten_days_later
    
    # Unloading date should be after loading date
    assert order.unloading_date > order.loading_date
    assert order.unloading_date <= order.loading_date + timedelta(days=5)


def test_different_countries_for_pickup_delivery(generator):
    order = generator.generate()
    # Pickup should be from a random European country
    assert order.pickup_address.country in generator.european_countries
    # Delivery should be in the UK
    assert order.delivery_address.country == "United Kingdom"
