from src.forecaster import Forecaster
from neuralprophet import NeuralProphet
from src.data_fetcher import DataFetcher
import os
import pandas as pd


def test_init():
    forecaster = Forecaster("91b65ab1-7509-450b-8910-30a1e9227cc4")
    assert forecaster.data_fetcher.site_id == "91b65ab1-7509-450b-8910-30a1e9227cc4"
    assert isinstance(forecaster.data_fetcher, DataFetcher)
    assert isinstance(forecaster.model, NeuralProphet)


def test_forecast():
    forecaster = Forecaster("91b65ab1-7509-450b-8910-30a1e9227cc4")
    forecaster.forecast()
    assert os.path.exists(
        "data/forecasted_flow/roaring_fork_river_blw_maroon_creek_nr_aspen_co_forecast.csv"
    )

def test_get_df():
    forecaster = Forecaster("91b65ab1-7509-450b-8910-30a1e9227cc4")
    df = forecaster._get_df()
    assert isinstance(df, pd.DataFrame)
    assert df.columns.tolist() == ["ds", "y"]
    assert df.dtypes[0] == "datetime64[ns]"
    assert df.dtypes[1] == "float64"

def test_get_site_source_name():
    forecaster = Forecaster("91b65ab1-7509-450b-8910-30a1e9227cc4")
    source_name = forecaster._get_site_source_name()
    assert source_name == "roaring_fork_river_blw_maroon_creek_nr_aspen_co"
    
