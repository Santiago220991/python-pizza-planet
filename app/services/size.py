from app.common.http_methods import GET, POST, PUT
from flask import Blueprint, request

from ..controllers import SizeController
from .base import BaseService

size = Blueprint("size", __name__)


@size.route("/", methods=POST)
def create_size():
    return BaseService.base_service(SizeController.create(request.json))


@size.route("/", methods=PUT)
def update_size():
    return BaseService.base_service(SizeController.update(request.json))


@size.route("/id/<_id>", methods=GET)
def get_size_by_id(_id: int):
    return BaseService.base_service(SizeController.get_by_id(_id))


@size.route("/", methods=GET)
def get_sizes():
    return BaseService.base_service(SizeController.get_all())
