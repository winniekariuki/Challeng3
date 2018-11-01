import datetime
import json
from functools import wraps

import jwt
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource
from werkzeug.security import check_password_hash, generate_password_hash

from app.api.v2.models import PostProduct, User, PostSale    
from instance.config import Config
from app.api.v2.utilis import *

from .db_conn import dbconn as conn

from flask_expects_json import expects_json
from app.api.v2.schemas import signup_schema,login_schema,product_schema,sale_schema


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
            print(data)
            for user in users:
                if user['username'] == data['username']:
                    user_data = user
                    print(user)
        except Exception as st:
            return make_response(jsonify({"message": "Invalid Token!"}), 403)

        return f(user_data, *args, **kwargs)
    return decorator

    

class UserAccount(Resource):
    @expects_json(signup_schema)
    @token_required
    def post(user_data,self):
        if user_data["role"] != "Admin":
            return make_response(jsonify({
                "message": "Not authorized"
            }), 401)

        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        role = data['role']

        valid = Register()
        valid.empty_validate(data)

        valid = Register()
        valid.email_validate(data)

        valid = Register()
        valid.existing_user(data)

        valid = Register()
        valid.pass_validate(data)

       

        valid = Register()
        valid.data_validate(data)

        

        valid = Register()
        valid.space_validate(data)
        
        admin = User(data)
        admin.save_admin() 

        user1 = User(data)
        print(user1)
        user1.save()
        # users = user1.get_users()

        return make_response(jsonify({
            "Status": "Ok",
            "Message": " registered successfully ",
            "username": data["username"],
            "email":data["email"],
            "role": data["role"]
        }), 201)

