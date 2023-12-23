import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


class Forecast:
    def __init__(self, df: pd.DataFrame, site_id: str) -> None:
        self.df = df
        self.site_id = site_id

    def save(self) -> None:
        Session = sessionmaker(bind=create_engine(os.getenv("DATABASE_URL")))
        with Session() as session:
            raw_sql = self._generate_raw_sql()
            session.execute(text(raw_sql))
            session.commit()

    def _generate_raw_sql(self) -> str:
        forecast_df = self._parse_dataframe()
        return self._dataframe_to_sql(forecast_df)

    def _dataframe_to_sql(self, df) -> str:
        values = self._format_values(df)
        return (
            f"INSERT INTO rr.forecast(site_id, ts, value) VALUES {values}"
            "ON CONFLICT (site_id, ts) DO UPDATE SET value = EXCLUDED.value;"
        )

    def _format_values(self, df) -> str:
        values = []
        for _idx, row in df.iterrows():
            values.append(f"('{row['site_id']}', '{row['ts']}', {row['value']})")
        return ", ".join(values)

    def _parse_dataframe(self) -> pd.DataFrame:
        forecast_df = self.df.copy(deep=True)
        forecast_df["site_id"] = self.site_id
        forecast_df.rename(columns={"predicted_mean": "value"}, inplace=True)
        forecast_df["value"] = forecast_df["value"].apply(lambda x: round(x, 2))
        forecast_df["value"] = forecast_df["value"].apply(lambda x: max(x, 0))
        forecast_df["ts"] = forecast_df.index
        forecast_df["ts"] = forecast_df["ts"].dt.strftime("%Y-%m-%d %H:%M:%S.%f %z")
        forecast_df = forecast_df.reset_index(drop=True)
        forecast_df = forecast_df[["site_id", "ts", "value"]]
        return forecast_df


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from src.flow_site import FlowSite
    from src.forecaster import Forecaster

    site_id = "dadf4f4e-2fbc-49c3-ae24-4313429e6e3b"
    Session = sessionmaker(bind=create_engine(os.getenv("DATABASE_URL")))
    with Session() as session:
        flow_site = FlowSite.for_id(site_id, session)
        forecaster = Forecaster(flow_site)
        forecast = forecaster.generate_forecast()
        parsed_df = forecast._parse_dataframe()
        print(parsed_df)
