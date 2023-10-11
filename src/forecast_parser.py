import pandas as pd
import datetime as dt
import os

class ForecastParser:
    def __init__(self):
        self.curent_datetime = self._get_current_datetime()

    def parse_forecast(self, csv_filepath) -> None:
        forecast_df = pd.read_csv(csv_filepath)
        forecast_df = forecast_df[forecast_df["ds"] > self.curent_datetime]
        forecast_df = forecast_df[["ds", "yhat1"]]
        forecast_df["yhat1"] = forecast_df["yhat1"].round(2)
        forecast_df["site_id"] = self._get_forecast_site_id(csv_filepath)
        forecast_df = forecast_df[["site_id", "ds", "yhat1"]]
        forecast_df = forecast_df.reset_index(drop=True).rename(columns={"ds": "ts", "yhat1": "value"})
        return forecast_df

    def _get_forecast_site_id(self, csv_filepath) -> str:
        return os.path.basename(csv_filepath).split(".")[0]
    
    def _get_current_datetime(self):
        current_datetime = dt.datetime.now()
        return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    forecast_parser = ForecastParser()
    print(forecast_parser.parse_forecast("data/forecasted_flow/0dba0e9f-1ac7-4fe7-8c50-82a0ec09becb.csv"))
