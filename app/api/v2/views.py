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


class LoginUser(Resource):
    @expects_json(login_schema)
    def post(self):
        self.user_ins = User.get_users(self)
        # print(self.user_ins)
        data = request.get_json()
        username = data["username"]
        password = data["password"]

        if not data or not username or not password:
            return make_response(jsonify({
                                         'Status': 'Failed',
                                         'Message': "Enter credentials"
                                         }), 400)

        for user in self.user_ins:
            print(user)
            if user['username'] == username and check_password_hash(user['password'], password):

                token = jwt.encode({'username': user['username'],
                                    'exp': datetime.datetime.utcnow() +
                                    datetime.timedelta(minutes=30)},
                                    Config.SECRET_KEY)
                return make_response(jsonify({'message':'You are successfully logged in',
                                             'token': token.decode('UTF-8')
                                             }), 200)

        return make_response(jsonify({
                
                'Message': "Please check your password and username"
                }), 403)


class Produce(Resource):
    @expects_json(product_schema)
    @token_required
    def post(user_data, self):
        if user_data["role"] != "Admin":
            return make_response(jsonify({
                "message": "Not authorized"
            }), 401)
        data = request.get_json()
        name = data['name'].strip("")
        category = data['category'].strip("")
        price = data['price'].strip("")
        quantity = data['quantity'].strip("")
        lower_inventory = data['lower_inventory'].strip("")
        date = datetime.datetime.now()

        
        valid = Validateproduct()
        valid.emptydetails(data)
        # valid = Validateproduct()
        # valid.detailsvalidate(data)

        valid = Register()
        valid.existing_product(data)

       

        product1 = PostProduct(data)
        product1.save_product()

        return make_response(jsonify({
            "Status": "Ok",
            "Message": "created successfully",
            "Myproduce": data}), 201)

    def get(self):
        product_ins = PostProduct.get_products(self)
        return make_response(jsonify({

            "Myproduce": product_ins}), 200)


class Singleproduct(Resource):
    @token_required
    def put(user_data, self, id):
        if user_data["role"] != "Admin":
           return make_response(jsonify({
               "message": "Not authorized"
           }), 401)
        self.product_ins = PostProduct.get_products(self)
        for product in self.product_ins:
            if int(product['id']) == int(id):
                data = request.get_json()
                product1 = PostProduct()
                product1.update_product(data, id)

                return make_response(jsonify({
                    
                    "Message": "Updated successfully"}), 200)

    @token_required
    def delete(user_data, self, id):
        if user_data["role"] != "Admin":
                return make_response(jsonify({
                    "message": "Not authorized"
                }), 401)
        self.product_ins = PostProduct.get_products(self)
        for product in self.product_ins:
            if int(product['id']) == int(id):
                product1 = PostProduct()
                product1.delete_product(id)
                return make_response(jsonify({
                    "Status": "Ok",
                    "Message": "deleted successfully"}), 200)

    def get(self,id):
        self.product_ins = PostProduct.get_products(self)
        print(self.product_ins)
        for product in self.product_ins:
            if int(product['id']) == int(id):
                return make_response(jsonify({
                    "Status": "Ok",
                    "Message": "successfully ",
                    "Myproducts": product}), 200)
        return make_response(jsonify({
            "Status": "Failed",
            "Message": "No such product "}), 404)


class SaleRecord(Resource):
    @expects_json(sale_schema)
    @token_required
    def post(user_data, self):
        if user_data["role"] != "storeattendant":
            return make_response(jsonify({
               "message": "Not authorized"
           }), 401)
        data = request.get_json()
        
        id = data['id']
        user_id = data['user_id']
        quantity = data['quantity']
        

        product = PostProduct.get_product_by_id(self, id)
        print(product)
        if not product:
            return make_response(jsonify({
                    "Message": "Product does not exist"}), 400)
        if product[4]<quantity:
            return make_response(jsonify({
                    "Message": "Product not enough"}), 400)
        if product[4]<0:
            return make_response(jsonify({
                    "Message": "Product is out of stock"}), 400)
     
        total_price=product[3]*quantity
        data = {
                "id": id,
                "user_id":user_id,
                "quantity":quantity,
                "total_price":total_price
            }
        sale1 = PostSale(data)
        new_quantity=product[4]-quantity
        PostProduct.update_product_quantity(self,id,new_quantity)
        sale1.save_sales()

        return make_response(jsonify({
            "Status": "Ok",
            "Message": "created successfully",
            "MySaleRecords": data}), 201)

    @token_required
    def get(user_data,self):
        if user_data["role"] != "Admin":
           return make_response(jsonify({
               "message": "Not authorized"
           }), 401)
        sale_ins = PostSale.get_sales(self)
        return make_response(jsonify({
            "Status": "Ok",
            "Message": "Success",
            "MySaleRecords": sale_ins}), 200)

class SingleSaleRecord(Resource):
        @token_required
        def get(user_data, self, saleID):
            if user_data["role"] != "Admin" or user_data["role"] != "storeattendant":
                    make_response(jsonify({
                        "message": "Unauthorized"
                    }), 401)
            self.sale_ins = PostSale.get_sales(self)
            for sale in self.sale_ins :
                if sale['sale_id'] == int(saleID):

                    return make_response(jsonify({
                        "Status": "Ok",
                        "Message": "Success",
                        "MySaleRecords": sale

                    }), 200)

        


        
