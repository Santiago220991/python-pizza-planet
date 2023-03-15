from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import IngredientController
from .base import BaseService

ingredient = Blueprint('ingredient', __name__)


@ingredient.route('/', methods=POST)
def create_ingredient():
    return BaseService.base_service(IngredientController.create(request.json))


@ingredient.route('/', methods=PUT)
def update_ingredient():
    return BaseService.base_service(IngredientController.update(request.json))


@ingredient.route('/id/<_id>', methods=GET)
def get_ingredient_by_id(_id: int):
    return BaseService.base_service(IngredientController.get_by_id(_id))


@ingredient.route('/', methods=GET)
def get_ingredients():
    return BaseService.base_service(IngredientController.get_all())
