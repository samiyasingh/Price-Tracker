import pandas as pd
from db_connection import get_connection

conn = get_connection()

df = pd.read_sql("SELECT product_name FROM products", conn)
conn.close()

print("Available products:\n")
print(df)
