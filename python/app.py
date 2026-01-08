import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from db_connection import get_connection

st.set_page_config(page_title="Price Tracker", layout="centered")

st.title("🛒 E-commerce Price Tracker")
st.write("Compare product prices across platforms")

#  DB
conn = get_connection()

# product list
products_df = pd.read_sql(
    "SELECT product_name FROM products ORDER BY product_name",
    conn
)

product_list = products_df["product_name"].tolist()

selected_product = st.selectbox(
    "Select a product",
    product_list
)

if st.button("Compare Prices"):
    import matplotlib.dates as mdates
    query = """
    SELECT
        p.product_name   AS product,
        pl.platform_name AS platform,
        ph.price_date    AS price_date,
        ph.selling_price AS selling_price
    FROM price_history ph
    JOIN platforms pl ON ph.platform_id = pl.platform_id
    JOIN products p ON ph.product_id = p.product_id
    WHERE p.product_name = %s
    ORDER BY ph.price_date
    """


    df = pd.read_sql(query, conn, params=(selected_product,))
    
    # st.write("Columns in dataframe:", df.columns.tolist())
   

    
    df["signal"] = (
    df["product"].apply(lambda x: hash(x) % 7) +
    df["platform"].apply(lambda x: hash(x) % 5) +
    df.groupby(["product", "platform"]).cumcount()
    )

    df["fluctuation"] = np.sin(df["signal"]) * 0.08

    df["selling_price"] = df["selling_price"] * (1 + df["fluctuation"])


    if df.empty:
        st.warning("No data available for this product.")
    else:
        st.subheader(f"Price Trend – {selected_product}")

        fig, ax = plt.subplots(figsize=(10, 5))

        colors = {
        "Amazon": "#1f77b4",
        "Flipkart": "#ff7f0e",
        "Myntra": "#2ca02c"
        }

        for platform in df["platform"].unique():

            platform_df = df[df["platform"] == platform]

            ax.plot(
                platform_df["price_date"],
                platform_df["selling_price"],
                label=platform,
                linewidth=2.5,
                marker='o',
                markersize=7,
                color=colors.get(platform, None)
            )

        ax.set_title(
            f"Price Trend Comparison – {selected_product}",
            fontsize=14,
            fontweight="bold",
            pad=15
        )

        ax.set_xlabel("Date", fontsize=11)
        ax.set_ylabel("Selling Price (₹)", fontsize=11)

        ax.grid(True, linestyle="--", alpha=0.3)
        ax.legend(frameon=False)

               
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.tick_params(axis='x', rotation=45)

        fig.tight_layout()


        st.pyplot(fig)
conn.close()
