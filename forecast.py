import pandas as pd
from prophet import Prophet

def prepare_data(df, sku):
    df = df[df['sku'] == sku].copy()
    df = df.rename(columns={'date': 'ds', 'sales': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])
    return df

def forecast_demand(df, periods):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
