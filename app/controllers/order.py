from app.controllers.validate_order import (
    OrderValidatorProxy,
    OrderValidator,
    OrderService,
)
from ..repositories.managers import OrderManager
from .base import BaseController


class OrderController(BaseController):
    manager = OrderManager
    __required_info = (
        "client_name",
        "client_dni",
        "client_address",
        "client_phone",
        "size_id",
    )

    @staticmethod
    def calculate_order_price(
        size_price: float, ingredients: list, beverages: list
    ):
        price = (
            size_price
            + sum(ingredient.price for ingredient in ingredients)
            + sum(beverage.price for beverage in beverages)
        )
        return round(price, 2)

    @classmethod
    def create(cls, order: dict):
        current_order = order.copy()
        order_validator = OrderValidator(
            current_order, cls.__required_info, cls
        )
        order_request: OrderService = OrderValidatorProxy(
            order_validator, current_order, cls.__required_info
        )
        return order_request.create()
