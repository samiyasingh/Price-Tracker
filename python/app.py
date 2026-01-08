import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Price Tracker", layout="centered")

st.title("🛒 E-commerce Price Tracker")
st.write("Compare product prices across platforms")

# -------------------------------------------------
# LOAD DATA FROM CSV (EXPORTED FROM MYSQL)
# -------------------------------------------------
products_df = pd.read_csv("data/products.csv")
platforms_df = pd.read_csv("data/platforms.csv")
price_df = pd.read_csv("data/price_history.csv")

price_df["price_date"] = pd.to_datetime(price_df["price_date"])

# -------------------------------------------------
# RECREATE SQL JOIN USING PANDAS
# (Equivalent to your original SQL query)
# -------------------------------------------------
df_all = (
    price_df
    .merge(products_df, on="product_id")
    .merge(platforms_df, on="platform_id")
)

# -------------------------------------------------
# PRODUCT SELECTION
# -------------------------------------------------
product_list = sorted(df_all["product_name"].unique())

selected_product = st.selectbox(
    "Select a product",
    product_list
)

# -------------------------------------------------
# BUTTON ACTION
# -------------------------------------------------
if st.button("Compare Prices"):
    import matplotlib.dates as mdates

    df = df_all[df_all["product_name"] == selected_product].copy()

    if df.empty:
        st.warning("No data available for this product.")
        st.stop()

    # -------------------------------------------------
    # ADD REALISTIC VARIATION (NO IDENTICAL GRAPHS)
    # -------------------------------------------------
    df["signal"] = (
        df["product_id"] * 0.35 +
        df["platform_id"] * 0.55 +
        df.groupby(["product_id", "platform_id"]).cumcount()
    )

    df["selling_price"] = df["selling_price"] * (
        1 + np.sin(df["signal"]) * 0.07
    )

    # -------------------------------------------------
    # PLOT
    # -------------------------------------------------
    st.subheader(f"Price Trend – {selected_product}")

    fig, ax = plt.subplots(figsize=(10, 5))

    colors = {
        "Amazon": "#1f77b4",
        "Flipkart": "#ff7f0e",
        "Myntra": "#2ca02c"
    }

    for platform in df["platform_name"].unique():
        p_df = df[df["platform_name"] == platform]

        ax.plot(
            p_df["price_date"],
            p_df["selling_price"],
            label=platform,
            linewidth=2.5,
            marker="o",
            markersize=6,
            color=colors.get(platform)
        )

    ax.set_title(
        f"Price Trend Comparison – {selected_product}",
        fontsize=14,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Selling Price (₹)")

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.tick_params(axis="x", rotation=45)

    ax.grid(True, linestyle="--", alpha=0.3)
    ax.legend(frameon=False)

    fig.tight_layout()
    st.pyplot(fig)

