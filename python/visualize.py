import pandas as pd
import matplotlib.pyplot as plt

from db_connection import get_connection

conn = get_connection()

query = """
SELECT 
    p.product_name,
    ph.price_date,
    ph.selling_price
FROM price_history ph
JOIN products p ON ph.product_id = p.product_id
WHERE p.product_name = 'Boat Rockerz 450 Headphones'
ORDER BY ph.price_date
"""

df = pd.read_sql(query, conn)
conn.close()

plt.figure()
plt.plot(df["price_date"], df["selling_price"], marker='o')
plt.title("Price Trend – Boat Rockerz 450 Headphones")
plt.xlabel("Date")
plt.ylabel("Selling Price")
plt.grid(True)
plt.show()
