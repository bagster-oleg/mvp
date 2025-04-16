import streamlit as st
import pandas as pd
from demand_forecasting import forecast_sku
from utils import parse_input_data, recommend_orders

st.set_page_config(page_title="AI-прогноз спроса", layout="wide")

st.title("📈 AI-прогноз спроса и рекомендации по закупкам")

uploaded_file = st.file_uploader("Загрузите CSV-файл", type=["csv", "xlsx"])

if uploaded_file:
    df_raw = parse_input_data(uploaded_file)

    st.success("✅ Файл успешно загружен!")
    skus = df_raw["sku"].unique()
    selected_sku = st.selectbox("Выберите SKU", skus)

    forecast_horizon = st.radio("Горизонт прогноза", [7, 14, 30], horizontal=True)
    lead_time = st.number_input("⏱ Лаг поставки (в днях)", min_value=0, value=2)
    
    if st.button("🔮 Прогнозировать"):
        df_forecast, fig = forecast_sku(df_raw, selected_sku, forecast_horizon)
        st.pyplot(fig)

        current_stock = st.number_input("📦 Текущий остаток", min_value=0)
        suggested_qty = recommend_orders(df_forecast, current_stock, lead_time)
        
        st.markdown(f"### 📌 Рекомендация к заказу: **{suggested_qty} шт.**")
        st.dataframe(df_forecast)

