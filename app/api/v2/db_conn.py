import psycopg2
import psycopg2.extras
from sys import modules



if 'pytest' in modules:
    def dbconn():
        connection = psycopg2.connect(host="localhost",user="postgres",dbname="teststore",password="1234")
        return connection
else:
    def dbconn():
        connection = psycopg2.connect(host="localhost",user="postgres",dbname="storemanager",password="1234")

        return connection

def create_tables():
	tables = (  """
                CREATE TABLE IF NOT EXISTS users (
                user_id serial PRIMARY KEY,
                username varchar(30) not null,
                email varchar(100) not null,
                password varchar(250) not null,
                role varchar(20) not null
                )
                """,

                """
                CREATE TABLE IF NOT EXISTS products (id serial PRIMARY KEY,
                name varchar(30) not null,
                category varchar(30) not null,
                price float(4) not null,
                quantity int not null,
                lower_inventory int not null
                
                )
                """,

                """
                    CREATE TABLE IF NOT EXISTS sales (sale_id serial PRIMARY KEY,
                    user_id int  REFERENCES users(user_id) not null,
                    quantity int not null,
                    id int  REFERENCES products(id) not null,
                    total_price int not null                
                
                    )
                """
             )
	try:
		connection = dbconn()
		cursor = connection.cursor()
		for table in tables:
			cursor.execute(table)
		cursor.close()
		connection.commit()
		connection.close()

	except psycopg2.DatabaseError as x:
		print(x)


def destroy_tables():
        cursor = dbconn().cursor()

        sql = [
            """DROP TABLE IF EXISTS users CASCADE""",
            """DROP TABLE IF EXISTS products CASCADE""",
            """DROP TABLE IF EXISTS sales CASCADE""",
        ]

        for query in sql:
            cursor.execute(query)
        dbconn().commit()
        dbconn().close()
