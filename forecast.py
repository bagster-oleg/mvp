import pandas as pd
from prophet import Prophet

def prepare_data(df, sku):
    # Фильтруем по SKU и переименовываем колонки
    df = df[df['sku'] == sku].copy()
    df = df.rename(columns={'date': 'ds', 'sales': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])
    return df

def forecast_demand(df, periods):
    if len(df) < 30:
        raise ValueError("Недостаточно данных для прогнозирования (нужно хотя бы 30 дней).")

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)

    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
