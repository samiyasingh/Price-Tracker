import pandas as pd
from db_connection import get_connection

print("Starting script...")

conn = get_connection()
print("Connected to database")

query = "SELECT COUNT(*) AS cnt FROM price_history"
df_count = pd.read_sql(query, conn)

print("Row count in price_history:")
print(df_count)

query2 = """
SELECT 
    p.product_name,
    ph.price_date,
    ph.selling_price
FROM price_history ph
JOIN products p ON ph.product_id = p.product_id
ORDER BY ph.price_date
LIMIT 10
"""

df = pd.read_sql(query2, conn)
conn.close()

print("\nSample rows:")
print(df)
print("\nScript finished.")
