import pandas as pd

def parse_input_data(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df.columns = [c.lower().strip() for c in df.columns]
    df["date"] = pd.to_datetime(df["date"])
    df["sku"] = df["sku"].astype(str)
    df["sales"] = df["sales"].astype(float)
    return df

def recommend_orders(forecast_df, current_stock, lead_time):
    demand_until_delivery = forecast_df["forecast"].head(lead_time).sum()
    demand_total = forecast_df["forecast"].sum()
    
    needed_qty = max(0, round(demand_total - current_stock))
    if needed_qty == 0:
        return 0
    else:
        return needed_qty

