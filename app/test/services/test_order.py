import pytest


def test_create_order_service(create_order):
    order = create_order.json
    pytest.assume(create_order.status.startswith("200"))
    pytest.assume(order["detail"])
    pytest.assume(order["beverage_detail"])
    pytest.assume(order["size"])
    pytest.assume(order["_id"])
    pytest.assume(order["client_address"])
    pytest.assume(order["client_dni"])
    pytest.assume(order["client_name"])
    pytest.assume(order["client_phone"])
    pytest.assume(order["beverage_detail"])
    pytest.assume(order["size"])


def test_get_orders_by_id_service(client, create_order, order_uri):
    current_order = create_order.json
    response = client.get(f'{order_uri}id/{current_order["_id"]}')
    pytest.assume(response.status.startswith("200"))
    returned_ingredient = response.json
    for param, value in current_order.items():
        pytest.assume(returned_ingredient[param] == value)


def test_get_order_service(client, create_orders, order_uri):
    response = client.get(order_uri)
    pytest.assume(response.status.startswith("200"))
    returned_orders = {order["_id"]: order for order in response.json}
    for order in create_orders:
        pytest.assume(order.json["_id"] in returned_orders)


def test_create_order_service_with_invalid_size(
        create_order_with_invalid_size):
    order = create_order_with_invalid_size.json
    pytest.assume(order == "Invalid size")


def test_create_order_service_with_invalid_data(
        create_order_with_invalid_client_data):
    order = create_order_with_invalid_client_data.json
    pytest.assume(order == "Invalid payload")
