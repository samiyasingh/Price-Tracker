import pandas as pd
import matplotlib.pyplot as plt
from db_connection import get_connection

# ask user for product
product_name = input("Enter product name: ")

conn = get_connection()

query = """
SELECT
    pl.platform_name,
    ph.price_date,
    ph.selling_price
FROM price_history ph
JOIN platforms pl ON ph.platform_id = pl.platform_id
JOIN products p ON ph.product_id = p.product_id
WHERE p.product_name = %s
ORDER BY ph.price_date
"""

df = pd.read_sql(query, conn, params=(product_name,))
conn.close()

if df.empty:
    print("❌ No data found for this product.")
else:
    print(df)

    for platform in df["platform_name"].unique():
        platform_df = df[df["platform_name"] == platform]
        plt.plot(
            platform_df["price_date"],
            platform_df["selling_price"],
            marker='o',
            label=platform
        )

    plt.title(f"Price Comparison – {product_name}")
    plt.xlabel("Date")
    plt.ylabel("Selling Price")
    plt.legend()
    plt.grid(True)
    plt.show()
