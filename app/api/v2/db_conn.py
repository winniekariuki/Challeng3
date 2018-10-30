import psycopg2
import psycopg2.extras


def dbconn():
	connection = psycopg2.connect(
		host="localhost", user="postgres", dbname="storemanager", password="1234")
	return connection


def create_tables():
	tables = ("""
                CREATE TABLE IF NOT EXISTS users (
                user_id serial PRIMARY KEY,
                username varchar(30) not null,
                password varchar(250) not null,
                role varchar(10) not null
                )
                """,

           """
                CREATE TABLE IF NOT EXISTS products (product_id serial PRIMARY KEY,
                name varchar(30) not null,
                model_no varchar(100) not null,
                category varchar(30) not null,
                price float(4) not null,
                quantity int not null,
                lower_inventory int not null)

                """,

           """
                    CREATE TABLE IF NOT EXISTS sales (sale_id serial PRIMARY KEY,
                    attendant_id int REFERENCES users(user_id) not null,
                    product_id int REFERENCES products(product_id) not null
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
