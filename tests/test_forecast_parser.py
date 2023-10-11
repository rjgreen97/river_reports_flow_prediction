from src.forecast_parser import ForecastParser
import datetime as dt
import numpy as np

def test_init():
    forecast_parser = ForecastParser()
    current_datetime = dt.datetime.now()
    assert forecast_parser.curent_datetime == current_datetime.strftime("%Y-%m-%d %H:%M:%S")

def test_parse_forecast():
    forecast_parser = ForecastParser()
    df = forecast_parser.parse_forecast("data/forecasted_flow/0dba0e9f-1ac7-4fe7-8c50-82a0ec09becb.csv")
    assert df.columns.tolist() == ["site_id", "ts", "value"]
    assert type(df["site_id"][0]) == str
    assert type(df["ts"][0]) == str
    assert type(df["value"][0]) == np.float64

def test_get_forecast_site_id():
    forecast_parser = ForecastParser()
    site_id = forecast_parser._get_forecast_site_id("data/forecasted_flow/0dba0e9f-1ac7-4fe7-8c50-82a0ec09becb.csv")
    assert site_id == "0dba0e9f-1ac7-4fe7-8c50-82a0ec09becb"
