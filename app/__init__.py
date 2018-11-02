from flask import Flask 
from  flask_restful import Api
from app.api.v2.db_conn import create_tables

from instance.config import app_config

create_tables()


def create_app(config_name):
	app = Flask(__name__,instance_relative_config=True)
	app.config.from_pyfile('config.py')
	from app.api.v2 import version2 as v2
	

	app.register_blueprint(v2)

	return app
