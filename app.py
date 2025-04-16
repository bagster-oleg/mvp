import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from forecast import prepare_data, forecast_demand

# Настроим стиль для графиков
sns.set(style="whitegrid")

st.title("📦 Прогноз спроса и управление остатками")

# Загружаем файл с данными
uploaded_file = st.file_uploader("Загрузите CSV с данными о продажах", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['date'] = pd.to_datetime(df['date'])

    # Выбор SKU
    skus = df['sku'].unique()
    sku_selected = st.selectbox("Выберите SKU", skus)

    # Настройки прогноза
    forecast_period = st.selectbox("На сколько дней вперёд прогноз?", [7, 14, 30])
    lead_time = st.number_input("⏳ Лаг поставки (дней)", min_value=0, max_value=60, value=2)
    stock_on_hand = st.number_input("📦 Текущий остаток на складе", min_value=0, value=30)

    # Подготовка данных
    df_prepared = prepare_data(df, sku_selected)

    # Прогноз спроса
    forecast = forecast_demand(df_prepared, forecast_period)

    # Отображаем таблицу с прогнозом
    st.subheader("🔮 Прогноз спроса:")
    st.dataframe(forecast.tail(forecast_period).reset_index(drop=True))

    # График: Прогноз спроса с доверительными интервалами
    fig, ax = plt.subplots(figsize=(10, 6))

    # Основной график прогноза (yhat)
    ax.plot(forecast['ds'], forecast['yhat'], label='Прогноз', color='blue', linewidth=2)

    # Доверительные интервалы (yhat_lower, yhat_upper)
    ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='blue', alpha=0.2, label='Интервал доверия')

    # Настройки графика
    ax.set_title(f"Прогноз спроса для {sku_selected} на {forecast_period} дней", fontsize=16)
    ax.set_xlabel("Дата", fontsize=12)
    ax.set_ylabel("Продажи", fontsize=12)
    ax.legend()

    # Показываем график
    st.pyplot(fig)

    # График компонента: тренд и сезонность
    st.subheader("🌟 Компоненты прогноза")

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    ax2.plot(forecast['ds'], forecast['yhat'], label='Тренд (yhat)', color='blue', linewidth=2)
    ax2.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], alpha=0.2, label='Интервал доверия')

    ax2.set_title("Компоненты прогноза (Тренд и Интервалы)", fontsize=16)
    ax2.set_xlabel("Дата", fontsize=12)
    ax2.set_ylabel("Продажи", fontsize=12)
    ax2.legend()

    st.pyplot(fig2)

    # Закупка: рекомендации по заказу
    total_forecasted_demand = forecast.tail(forecast_period)['yhat'].sum()
    reorder_point = forecast.head(lead_time)['yhat'].sum()
    recommended_order = max(0, total_forecasted_demand - stock_on_hand)

    st.markdown("---")
    st.subheader("📊 Рекомендации:")
    st.markdown(f"**Прогноз спроса на {forecast_period} дней:** `{total_forecasted_demand:.1f}` ед.")
    st.markdown(f"**Рекомендуем заказать:** `{recommended_order:.1f}` ед. (учтён текущий остаток: {stock_on_hand}, лаг: {lead_time} дн)")
