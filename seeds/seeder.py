from flask_seeder import Faker, generator, Seeder
from faker import Faker as faker
from random import randint, choice, sample
from datetime import datetime
from seeds.ingredients import ingredients
from seeds.beverages import beverages
from seeds.sizes import sizes
from seeds.clients import clients

from app.repositories.models import (
    Order,
    Beverage,
    Ingredient,
    Size,
    OrderDetail,
    OrderBeverageDetail,
)
from app.plugins import db
from app.controllers import *


def create_sizes(data) -> list:
    return [Size(name=key, price=value) for key, value in data.items()]


def create_beverages(data) -> list:
    return [Beverage(name=key, price=value) for key, value in data.items()]


def create_ingredients(data) -> list:
    return [Ingredient(name=key, price=value) for key, value in data.items()]


def create_orders(count: int, clients) -> list:
    new_order = []
    order_detail = []
    beverage_order_detail = []
    fake = faker()
    ingredients, _ = IngredientController.get_all()
    sizes, _ = SizeController.get_all()
    beverages, _ = BeverageController.get_all()
    for index in range(1, count + 1):
        size = sizes[randint(0, len(sizes) - 1)]
        order_beverages = sample(beverages, randint(1, len(beverages) - 1))
        order_ingredients = sample(ingredients, randint(1, len(ingredients) - 1))
        name = clients[randint(0, len(clients) - 1)]
        total = (
            size["price"]
            + sum(ingredient["price"] for ingredient in order_ingredients)
            + sum(beverage["price"] for beverage in order_beverages)
        )
        new_order.append(
            Order(
                client_name=name,
                client_dni=fake.pyint(99999999, 999999999),
                client_phone=fake.pyint(99999999, 999999999),
                client_address=fake.address(),
                total_price=round(total, 2),
                date=fake.date_between(
                    datetime.fromisoformat("2023-01-01"),
                    datetime.fromisoformat(datetime.now().date().isoformat()),
                ),
                size_id=size["_id"],
            )
        )
        for ingredient in order_ingredients:
            order_detail.append(
                OrderDetail(
                    order_id=index,
                    ingredient_price=ingredient["price"],
                    ingredient_id=ingredient["_id"],
                )
            )

        for beverage in order_beverages:
            beverage_order_detail.append(
                OrderBeverageDetail(
                    order_id=index,
                    beverage_price=beverage["price"],
                    beverage_id=beverage["_id"],
                )
            )

    return new_order, order_detail, beverage_order_detail


class DatabaseSeeder(Seeder):
    @classmethod
    def run(self):
        size = create_sizes(sizes)
        beverage = create_beverages(beverages)
        ingredient = create_ingredients(ingredients)
        self.insert_db(size)
        self.insert_db(beverage)
        self.insert_db(ingredient)
        order, order_detail, beverage_order_detail = create_orders(100, clients)
        self.insert_db(order)
        self.insert_db(order_detail)
        self.insert_db(beverage_order_detail)

    def insert_db(data):
        for item in data:
            db.session.add(item)
