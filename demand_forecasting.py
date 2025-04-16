from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

def forecast_sku(df, sku, horizon):
    df_sku = df[df["sku"] == sku].copy()
    df_sku = df_sku.rename(columns={"date": "ds", "sales": "y"})
    df_sku = df_sku[["ds", "y"]]

    model = Prophet()
    model.fit(df_sku)

    future = model.make_future_dataframe(periods=horizon)
    forecast = model.predict(future)

    forecast_result = forecast[["ds", "yhat"]].tail(horizon)
    forecast_result = forecast_result.rename(columns={"ds": "date", "yhat": "forecast"})

    # Визуализация
    fig = model.plot(forecast)
    plt.title(f"Прогноз для {sku} на {horizon} дней")

    return forecast_result, fig

