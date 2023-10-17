from src.forecast import Forecast
from src.forecaster import Forecaster
import datetime as dt
import numpy as np
import pandas as pd


def test_init():
    forecaster = Forecaster("91b65ab1-7509-450b-8910-30a1e9227cc4")
    forecast = forecaster.generate_forecast()
    assert isinstance(forecast, Forecast)
    assert forecast.site_id == "91b65ab1-7509-450b-8910-30a1e9227cc4"
    assert forecast.engine.url.database == "riverreports"


def test_save():
    pass


def test_parse_forecast():
    forecaster = Forecaster("91b65ab1-7509-450b-8910-30a1e9227cc4")
    forecast = forecaster.generate_forecast()
    forecast_df = forecast._parse_forecast()
    assert isinstance(forecast_df, pd.DataFrame)
    assert forecast_df.columns.tolist() == ["site_id", "ts", "value"]
    assert forecast_df.dtypes[0] == "object"
    assert forecast_df.dtypes[1] == "datetime64[ns]"
    assert forecast_df.dtypes[2] == "float64"
