import streamlit as st
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Price Tracker", layout="centered")

st.title("🛒 E-commerce Price Tracker")
st.write("Compare product prices across platforms")

# ---------------- LOAD CSV DATA ----------------
products_df = pd.read_csv("../data/products.csv")
platforms_df = pd.read_csv("../data/platforms.csv")
price_history_df = pd.read_csv("../data/price_history.csv")


price_history_df["price_date"] = pd.to_datetime(price_history_df["price_date"])

# ---------------- PRODUCT LIST ----------------

product_list = ["— Select a product —"] + products_df["product_name"].tolist()

selected_product = st.selectbox(
    "Select a product",
    product_list
)

if st.button("Compare Prices"):
    if selected_product == "— Select a product —":
        st.warning("Please select a product first.")
        st.stop()

    # -------- SQL JOIN equivalent using pandas --------
    df = (
        price_history_df
        .merge(products_df, on="product_id")
        .merge(platforms_df, on="platform_id")
    )

    df = df[df["product_name"] == selected_product]

    df = df.rename(columns={
        "product_name": "product",
        "platform_name": "platform"
    })

    # ---------------- PRICE FLUCTUATION ----------------

    df["signal"] = (
        df["product"].apply(lambda x: hash(x) % 7)
        + df["platform"].apply(lambda x: hash(x) % 5)
        + df.groupby(["product", "platform"]).cumcount()
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
                marker="o",
                markersize=7,
                color=colors.get(platform)
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

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.tick_params(axis="x", rotation=45)

        fig.tight_layout()
        st.pyplot(fig)
