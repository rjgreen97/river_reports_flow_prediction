import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Forecast:
    def __init__(self, df: pd.DataFrame, site_id: str) -> None:
        self.df = df
        self.site_id = site_id
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
        forecast_df = self.df.copy(deep=True)
        forecast_df = forecast_df[["ds", "yhat1"]]
        forecast_df["yhat1"] = forecast_df["yhat1"].round(2)
        forecast_df["site_id"] = self.site_id
        forecast_df = forecast_df[["site_id", "ds", "yhat1"]]
        forecast_df = forecast_df.reset_index(drop=True).rename(
            columns={"ds": "ts", "yhat1": "value"}
        )
        return forecast_df


if __name__ == "__main__":
    from src.forecaster import Forecaster

    forecaster = Forecaster("91b65ab1-7509-450b-8910-30a1e9227cc4")
    forecast = forecaster.generate_forecast()
    df = forecast._parse_forecast()
    print(df)
