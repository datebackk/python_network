from app.database.models.user import User
from flask_restless import APIManager

v1_api_url_prefix = '/api/v1'

api_manager = APIManager()

api_manager.create_api(User, url_prefix=v1_api_url_prefix, methods=['GET', 'POST', 'DELETE', 'PATCH'], allow_delete_many=True)
