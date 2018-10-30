from datetime import datetime
from flask import jsonify, make_response
from instance.config import Config
from app.api.v2.db_conn import dbconn


class User():
    def __init__(self, data=None):
        self.con = dbconn()
        if data:
            self.username = data['username']
            self.password = data['password']
            self.role = data['role']

    def save(self):
        cursor = self.con.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username,password,role) VALUES (%s, %s, %s)",
                (self.username, self.password, self.role)
            )

        except Exception as e:
            print(e)
        self.con.commit()
        self.con.close()

   
        
