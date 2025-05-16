import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from forecast import prepare_data, forecast_demand

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

    # Обрезаем прогноз только на нужный период
    forecast_display = forecast.tail(forecast_period)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Строим график только для нужного периода
    ax.plot(forecast_display['ds'], forecast_display['yhat'], label='Прогноз', color='blue', linewidth=2)
    # Добавь в график линию исторических продаж:
    ax.plot(df_prepared['ds'], df_prepared['y'], label='Исторические продажи', color='gray', linestyle='--')

    ax.fill_between(forecast_display['ds'], forecast_display['yhat_lower'], forecast_display['yhat_upper'], color='blue', alpha=0.2, label='Интервал доверия')

    ax.set_title(f"Прогноз спроса для {sku_selected} на {forecast_period} дней", fontsize=16)
    ax.set_xlabel("Дата", fontsize=12)
    ax.set_ylabel("Продажи", fontsize=12)
    ax.legend()

    # Форматирование дат на оси X
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    st.pyplot(fig)


    # Настройки графика
    ax.set_title(f"Прогноз спроса для {sku_selected} на {forecast_period} дней", fontsize=16)
    ax.set_xlabel("Дата", fontsize=12)
    ax.set_ylabel("Продажи", fontsize=12)
    ax.legend()

    # Убедимся, что все даты отображаются на оси x
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()  # Автоматическая настройка наклона дат

    # Показываем график
    st.pyplot(fig)

    # Закупка: рекомендации по заказу
    total_forecasted_demand = forecast.tail(forecast_period)['yhat'].sum()
    reorder_point = forecast.head(lead_time)['yhat'].sum()
    recommended_order = max(0, total_forecasted_demand - stock_on_hand)

    st.markdown("---")
    st.subheader("📊 Рекомендации:")
    st.markdown(f"**Прогноз спроса на {forecast_period} дней:** `{total_forecasted_demand:.1f}` ед.")
    st.markdown(f"**Рекомендуем заказать:** `{recommended_order:.1f}` ед. (учтён текущий остаток: {stock_on_hand}, лаг: {lead_time} дн)")
    st.info("📘 *Интервал доверия* — это диапазон, в который с высокой вероятностью попадёт спрос. Например, 80% уверенность.")
    st.download_button("📥 Скачать прогноз (CSV)", forecast_display.to_csv(index=False), "forecast.csv", "text/csv")
