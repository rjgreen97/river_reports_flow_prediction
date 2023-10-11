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
        return forecast_df
    
    def _get_current_datetime(self):
        current_datetime = dt.datetime.now()
        return current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    def _get_all_csv_filepaths(self):
        csv_filepaths = []
        for root, _dirs, files in os.walk(os.path.join("data", "forecasted_flow")):
            for file in files:
                if file.endswith(".csv"):
                    csv_filepaths.append(os.path.join(root, file))
        return csv_filepaths


if __name__ == "__main__":
    forecast_parser = ForecastParser()
    print(forecast_parser.parse_forecast("data/forecasted_flow/allegheny_river_at_franklin_pa_forecast.csv"))
