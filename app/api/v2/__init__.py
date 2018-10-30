from flask_restful import Api
from flask import Blueprint

from app.api.v2.views import UserAccount

version2 = Blueprint('api', __name__, url_prefix='/api/v2')

api = Api(version2)
api.add_resource(UserAccount, '/auth/signup')
