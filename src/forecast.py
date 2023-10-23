import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.data_fetcher import DataFetcher


class Forecast:
    def __init__(self, df: pd.DataFrame, site_id: str) -> None:
        self.df = df
        self.site_id = site_id
        self.database_url = DataFetcher.get_database_url()
        self.engine = create_engine(self.database_url)

    def save(self) -> None:
        Session = sessionmaker(bind=self.engine)
        with Session() as session:
            raw_sql = self._generate_raw_sql()
            session.execute(text(raw_sql))
            session.commit()

    def _generate_raw_sql(self) -> str:
        forecast_df = self._parse_dataframe()
        return self._dataframe_to_sql(forecast_df)

    def _dataframe_to_sql(self, df) -> str:
        values = self._format_values(df)
        return f"INSERT INTO rr.forecast(site_id, ts, value) VALUES {values} ON CONFLICT (site_id, ts) DO UPDATE SET value = EXCLUDED.value;"

    def _format_values(self, df) -> str:
        values = []
        for _idx, row in df.iterrows():
            values.append(f"('{row['site_id']}', '{row['ts']}', {row['value']})")
        return ", ".join(values)

    def _parse_dataframe(self) -> pd.DataFrame:
        forecast_df = self.df.copy(deep=True)
        forecast_df = forecast_df[["ds", "yhat1"]]
        forecast_df["yhat1"] = forecast_df["yhat1"].round(2)
        forecast_df["yhat1"] = forecast_df["yhat1"].apply(lambda x: max(x, 0))
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
    df = forecast._parse_dataframe()
    values = forecast._format_values(df)
    print("\n=========================")
    print(f"values: {values}")
    print("=========================")
