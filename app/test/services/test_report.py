import pytest

def test_create_order_by_id_service(client, create_orders, report_uri):
    response=client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    pytest.assume(response.json['best_clients'])
    pytest.assume(response.json['month_with_the_higest_revenue'])
    pytest.assume(response.json['most_requested_ingredient'])
