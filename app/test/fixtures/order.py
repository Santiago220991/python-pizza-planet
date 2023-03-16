import pytest
import random

from ..utils.functions import (shuffle_list, get_random_sequence,
                               get_random_string)


def client_data_mock() -> dict:
    return {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence()
    }

def invalid_client_data_mock() -> dict:
    data = {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_sequence()
    }
    random_element=random.sample(list(data),1)[0]
    del data[random_element]
    return data

@pytest.fixture
def order_uri():
    return '/order/'


@pytest.fixture
def client_data():
    return client_data_mock()


@pytest.fixture
def create_order(client, order_uri, create_ingredients, create_beverages, create_size) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    size_id = (create_size.json).get('_id')
    response = client.post(order_uri, json={
        **client_data_mock(),
        'ingredients': ingredients,
        'beverages': beverages,
        'size_id': size_id
    })
    return response


@pytest.fixture
def create_orders(client, order_uri, create_ingredients, create_beverages, create_sizes) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    sizes = [size.get('_id') for size in create_sizes]
    orders = []
    for _ in range(10):
        new_order = client.post(order_uri, json={
            **client_data_mock(),
            'ingredients': shuffle_list(ingredients)[:5],
            'beverages': shuffle_list(beverages)[:5],
            'size_id': shuffle_list(sizes)[0]
        })
        orders.append(new_order)
    return orders


@pytest.fixture
def create_order_with_invalid_size(client, order_uri, create_ingredients, create_beverages) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    size_id = "XX"
    response = client.post(order_uri, json={
        **client_data_mock(),
        'ingredients': ingredients,
        'beverages': beverages,
        'size_id': size_id
    })
    return response


@pytest.fixture
def create_order_with_invalid_client_data(client, order_uri, create_ingredients, create_beverages, create_size) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    size_id = (create_size.json).get('_id')
    response = client.post(order_uri, json={
        **invalid_client_data_mock(),
        'ingredients': ingredients,
        'beverages': beverages,
        'size_id': size_id
    })
    return response