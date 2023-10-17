import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Forecast:
    def __init__(self, df: pd.DataFrame, site_id: str) -> None:
        self.df = df
        self.site_id = site_id
        self.current_datetime = self._get_current_datetime()
        self.engine = create_engine("postgresql://rjgreen@localhost/riverreports")

    # def save(self) -> None:
    #     Session = sessionmaker(bind=self.engine)
    #     try:
    #         forecast_df = self._parse_forecast()
    #         forecast_df.to_sql(
    #             "rr.forecast", con=self.session.bind, if_exists="append", index=False
    #         )

    #     except Exception as e:
    #         print(f"Error writing {self.site_id} to database: {e}")
    #     self.session.close()

    def _parse_forecast(self) -> pd.DataFrame:
        # forecast_df = forecast_df[forecast_df["ds"] > self.curent_datetime]
        forecast_df = self.df.copy(deep=True)
        forecast_df = forecast_df[["ds", "yhat1"]]
        forecast_df["yhat1"] = forecast_df["yhat1"].round(2)
        forecast_df["site_id"] = self.site_id
        forecast_df = forecast_df[["site_id", "ds", "yhat1"]]
        forecast_df = forecast_df.reset_index(drop=True).rename(
            columns={"ds": "ts", "yhat1": "value"}
        )
        return forecast_df

    def _get_current_datetime(self) -> str:
        current_datetime = dt.datetime.now()
        return current_datetime.strftime("%Y-%m-%d %H:%M:%S")
