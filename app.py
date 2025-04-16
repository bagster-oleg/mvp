import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from forecast import prepare_data, forecast_demand

st.title("📦 Прогноз спроса и управление остатками")

uploaded_file = st.file_uploader("Загрузите CSV с данными о продажах", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])

    skus = df['sku'].unique()
    sku_selected = st.selectbox("Выберите SKU", skus)

    forecast_period = st.selectbox("На сколько дней вперёд прогноз?", [7, 14, 30])

    lead_time = st.number_input("⏳ Лаг поставки (дней)", min_value=0, max_value=60, value=2)
    stock_on_hand = st.number_input("📦 Текущий остаток на складе", min_value=0, value=30)

    # загружаем файл, фильтруем по SKU
    df_prepared = prepare_data(df, sku_selected)

    # получаем прогноз
    forecast = forecast_demand(df_prepared, forecast_period)

    # отображаем результат
    st.subheader("🔮 Прогноз спроса:")
    st.dataframe(forecast.tail(forecast_period).reset_index(drop=True))

    # График
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(forecast['ds'], forecast['yhat'], label='Прогноз')
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2)
    ax.set_title(f"Прогноз спроса для {sku_selected}")
    ax.legend()
    st.pyplot(fig)

    # Закупка
    total_forecasted_demand = forecast.tail(forecast_period)['yhat'].sum()
    reorder_point = forecast.head(lead_time)['yhat'].sum()
    recommended_order = max(0, total_forecasted_demand - stock_on_hand)

    st.markdown("---")
    st.subheader("📊 Рекомендации:")
    st.markdown(f"**Прогноз спроса на {forecast_period} дней:** `{total_forecasted_demand:.1f}`")
    st.markdown(f"**Рекомендуем заказать:** `{recommended_order:.1f}` ед. (учтён текущий остаток: {stock_on_hand}, лаг: {lead_time} дн)")
