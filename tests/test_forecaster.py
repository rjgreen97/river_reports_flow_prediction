from src.forecaster import Forecaster
from src.flow_site import FlowSite
from src.forecast import Forecast
import os
import pandas as pd


def test_init():
    flow_site = FlowSite("91b65ab1-7509-450b-8910-30a1e9227cc4")
    forecaster = Forecaster(flow_site)
    assert forecaster.flow_site == flow_site


def test_generate_forecast():
    flow_site = FlowSite.for_id("91b65ab1-7509-450b-8910-30a1e9227cc4")
    forecaster = Forecaster(flow_site)
    forecast = forecaster.generate_forecast()
    assert isinstance(forecast, Forecast)
    assert forecast.df.shape == (7, 6)
