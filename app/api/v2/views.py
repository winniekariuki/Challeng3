from flask import make_response, request, jsonify
from flask import Flask
from flask_restful import Resource, Api
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
import json
from instance.config import Config
from .db_conn import dbconn as conn
from app.api.v2.models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        user_data = None
        user_ins = User()
        users = user_ins.get_users()
        if 'access_token' in request.headers:
             token = request.headers['access_token']

        if not token:
            return make_response(jsonify({
                "message": "Login!!"
            }), 401)
        try:
            data = jwt.decode(token, Config.SECRET_KEY)
            for user in users:
                if user['username'] == data['username']:
                    user_data = user
        except Exception as st:
            return (jsonify({"message": "Invalid Token!"}), 403)

        return f(user_data, *args, **kwargs)
    return decorator


class UserAccount(Resource):

    def post(self):
        data = request.get_json()
        user1 = User(data)
        user1.save()
        # users = user1.get_users()
        return make_response(jsonify({
            "Status": "Ok",
            "Message": " registered successfully "
        }), 201)


