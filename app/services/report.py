from app.common.http_methods import GET
from flask import Blueprint

from ..controllers import ReportController
from .base import BaseService

report = Blueprint('report', __name__)

@report.route('/', methods=GET)
def get_report():
    return BaseService.base_service(ReportController.create())


