from sqlalchemy.exc import SQLAlchemyError
from app.repositories.managers import (IngredientManager, OrderManager,
SizeManager, BeverageManager)
from typing import Tuple
from app.common.utils import check_required_keys

class OrderService():
    def create():
        raise NotImplementedError('Method not supported')

class OrderValidator(OrderService):
    current_order: dict
    required_info: Tuple

    def __init__ (self, current_order: dict, required_info: Tuple, cls):
        self.current_order=current_order
        self.required_info=required_info
        self.cls=cls

    def create(self):
        size_id = self.current_order.get('size_id')
        ingredient_ids = self.current_order.pop('ingredients', [])
        beverages_ids = self.current_order.pop('beverages', [])
        try:
            size = SizeManager.get_by_id(size_id)
            ingredients = IngredientManager.get_by_id_list(ingredient_ids)
            beverages = BeverageManager.get_by_id_list(beverages_ids)
            price = self.cls.calculate_order_price(size.get('price'), ingredients, beverages)
            order_with_price = {**self.current_order, 'total_price': price}
            return self.cls.manager.create(order_with_price, ingredients, beverages), None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)

class OrderValidatorProxy(OrderService):
    ordervalidator: OrderValidator
    current_order: dict
    required_info: Tuple

    def __init__ (self, ordervalidator:OrderValidator, current_order: dict, required_info: Tuple):
        self.ordervalidator=ordervalidator
        self.current_order=current_order
        self.required_info=required_info
        
    def create(self):
        if not self.checkSize():
            return "Invalid size", None
        if not self.checkPayload():
            return "Invalid payload", None
        return self.ordervalidator.create()

    def checkSize(self):
        size_id = self.current_order.get('size_id')
        size = SizeManager.get_by_id(size_id)
        if not size:
            return False
        return True

    def checkPayload(self):
        if not check_required_keys(self.required_info, self.current_order):
            return False
        return True