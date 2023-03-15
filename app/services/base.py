from flask import jsonify

class BaseService:
    def base_service ( controller_action ):
        entity, error = controller_action
        response = entity if not error else {'error': error}
        status_code = 200 if not error else 400
        return jsonify(response), status_code