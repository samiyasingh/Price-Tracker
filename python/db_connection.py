import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Saagnik@007",
        database="price_tracker"
    )
