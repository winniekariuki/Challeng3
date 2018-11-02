from datetime import datetime
from flask import jsonify,make_response
from instance.config import Config
from app.api.v2.db_conn import dbconn
from werkzeug.security import check_password_hash, generate_password_hash



class User():
    def __init__(self, data=None):
        
        if data:
            self.con=dbconn()

            self.username = data['username']
            self.email = data['email']
            self.password =generate_password_hash(data['password'])
            self.role = data['role']
            print(data)

    def save_admin(self):
        '''Save the admin information in the database'''
        cur = self.con.cursor()
        try:
            password=str(generate_password_hash("winnie07@"))
            print(password)
            cur.execute(
               " INSERT INTO users(username, email, password, role)"
               """VALUES('Winnie', 'winniekariuki07@gmail.com',
                    %s, 'Admin')""",(password,)

            )
        except Exception as s:
            print(s)
        self.con.commit()
        self.con.close()


    def save(self):
        '''Save the users information in the database'''
        cur = self.con.cursor()
        try:
            cur.execute(
            "INSERT INTO users (username,email,password, role) VALUES (%s, %s, %s,%s)",
            (self.username,self.email, self.password, self.role)

                )
        except Exception as s:
            print(s)
        self.con.commit()
        self.con.close()
        




    def get_users(self):
        self.con=dbconn()
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()        
    
        users = []
        

        for user in result:
            single_user = {}
            single_user['user_id'] = user[0]
            single_user['username'] = user[1]
            single_user['email'] = user[2]
            single_user['password'] = user[3]
            single_user['role'] = user[4]
            users.append(single_user)

            self.con.close()
        # print(users)
        return users


class PostProduct():
    def __init__(self, data=None):
        if data:
            self.con = dbconn()

            self.name = data['name']
            self.category = data['category']
            self.price = data['price']
            self.quantity = data['quantity']
            self.lower_inventory = data['lower_inventory']
            

    def save_product(self):
        
        cursor = self.con.cursor()
        
        try:
            cursor.execute(
            "INSERT INTO products(name,category,price,quantity,lower_inventory) VALUES(%s,%s,%s,%s,%s)",
            (self.name, self.category, self.price,self.quantity,self.lower_inventory)


                )
        except Exception as f:
            print(f)
        self.con.commit()
        self.con.close()
        
    
    def get_products(self):
        self.con=dbconn() 

        cursor = self.con.cursor()
        cursor.execute("SELECT  * FROM products")
        result = cursor.fetchall()
        # print(result)
        products = []

        for product in result:
            single_product = {}
            single_product['id'] =product[0]
            single_product['name'] =product[1]
            single_product['category'] =product[2]
            single_product['price'] =product[3]
            single_product['quantity'] =product[4]
            single_product['lower_inventory'] =product[5]
            
            

            products.append(single_product)

        self.con.close()
        return products

            

    def update_product(self, data,id):
        name = data['name']
        category = data['category']
        price = data['price']
        quantity = data['quantity']
        lower_inventory = data['lower_inventory']
        self.con=dbconn() 
        cursor = self.con.cursor()
        try:
            cursor.execute(
                "UPDATE products SET name = %s,price = %s,quantity = %s,category=%s, lower_inventory = %s WHERE id = %s",
                (name, price,quantity, category,lower_inventory,id)
            )
        except Exception as e:
            print(e)
        self.con.commit()
        self.con.close()

    def delete_product(self,id):
        self.id = id
        self.con=dbconn() 
        cursor = self.con.cursor()
        cursor.execute(
            "DELETE FROM products WHERE id = %s",
            (self.id)

            )
        self.con.commit()
        self.con.close()

    def get_product_by_id(self,id):
        self.con=dbconn() 
        cursor = self.con.cursor()
        cursor.execute(
            "SELECT * FROM products WHERE id = %s",
            (id,)

            )
        product=cursor.fetchone()
        self.con.commit()
        self.con.close()
        return product

    def update_product_quantity(self,id,new_quantity):
        self.con=dbconn() 
        cursor = self.con.cursor()
        cursor.execute(
            "UPDATE products SET quantity = %s WHERE id = %s RETURNING quantity",
            (new_quantity, id,)
            )
        updated_product=cursor.fetchone()
        self.con.commit()
        self.con.close() 
        return updated_product
 
class PostSale():
    def __init__(self, data=None):
        if data:
            self.con = dbconn()

            self.user_id = data['user_id']
            self.id = data['id']
            self.quantity = data['quantity']
            self.total_price = data['total_price']
        
            

    def save_sales(self):
        
        cursor = self.con.cursor()
        
        try:
            cursor.execute(
            "INSERT INTO sales(user_id,id,quantity,total_price) VALUES(%s,%s,%s,%s)",
            (self.user_id, self.id, self.quantity, self.total_price,)


                )
        except Exception as y:
            print(y)
        self.con.commit()
        self.con.close()
        

    def get_sales(self):
    
        self.con=dbconn() 

        cursor = self.con.cursor()
        cursor.execute("SELECT  * FROM sales")
        result = cursor.fetchall()
        # print(result)
        sales = []

        for sale in result:
            single_sale = {}
            single_sale['sale_id'] = sale[0]
            single_sale['user_id'] =sale[1]
            single_sale['id'] =sale[2]
            
            sales.append(single_sale)

            self.con.close()
            return sales
    







