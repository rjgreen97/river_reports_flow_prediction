from src.forecast import Forecast
import pandas as pd

def create_df():
    data = {
        "ds": [
            "2023-09-28",
            "2023-09-29",
            "2023-09-30",
        ],
        "y": [None, None, None],
        "yhat1": [
            214.205597,
            218.915924,
            219.206116,
        ],
        "trend": [
            367.802521,
            368.137421,
            368.472198,
        ],
        "season_yearly": [
            -156.960495,
            -154.905975,
            -152.800049,
        ],
        "season_weekly": [
            3.363567,
            5.684486,
            3.533973,
        ],
    }
    return pd.DataFrame(data)

def test_init():
    df = create_df()
    forecast = Forecast(df, "91b65ab1-7509-450b-8910-30a1e9227cc4")
    assert isinstance(forecast, Forecast)
    assert forecast.site_id == "91b65ab1-7509-450b-8910-30a1e9227cc4"


def test_generate_raw_sql():
    df = create_df()
    forecast = Forecast(df, "91b65ab1-7509-450b-8910-30a1e9227cc4")
    sql = forecast._generate_raw_sql()
    assert (
        sql
        == "INSERT INTO rr.forecast(site_id, ts, value) VALUES ('91b65ab1-7509-450b-8910-30a1e9227cc4', '2023-09-28', 214.21), ('91b65ab1-7509-450b-8910-30a1e9227cc4', '2023-09-29', 218.92), ('91b65ab1-7509-450b-8910-30a1e9227cc4', '2023-09-30', 219.21) ON CONFLICT (site_id, ts) DO UPDATE SET value = EXCLUDED.value;"
    )


def test_parse_dataframe():
    df = create_df()
    forecast = Forecast(df, "91b65ab1-7509-450b-8910-30a1e9227cc4")
    forecast_df = forecast._parse_dataframe()
    assert isinstance(forecast_df, pd.DataFrame)
    assert forecast_df.columns.tolist() == ["site_id", "ts", "value"]
    assert forecast_df.dtypes[0] == "object"
    assert forecast_df.dtypes[2] == "float64"
