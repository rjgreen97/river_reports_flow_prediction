from src.data_fetcher import DataFetcher
from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import os

set_log_level("ERROR")


class Forecaster:
    def __init__(self, site_id: str) -> None:
        self.data_fetcher = DataFetcher(site_id)
        self.model = NeuralProphet()
        self.df = self._get_df()
        self.source_name = self._get_site_source_name()

    def forecast(self) -> None:
        self.model.fit(self.df, freq="H")
        df_future = self.model.make_future_dataframe(
            self.df, n_historic_predictions=True, periods=365
        )
        forecast_df = self.model.predict(df_future)
        forecast_df.to_csv(os.path.join("data", "forecasted_flow", f"{self.source_name}_forecast.csv" ))

        plot = self.model.plot(forecast_df)
        plot.write_image(
            os.path.join("data", "forecasted_flow_plots", f"{self.source_name}_forecast.png")
        )

    def _get_df(self) -> pd.DataFrame:
        return self.data_fetcher.generate_df()

    def _get_site_source_name(self) -> str:
        return self.data_fetcher.source_name.lower().replace(" ", "_").replace(",", "")


if __name__ == "__main__":
    flow_forecaster = Forecaster("81b4b099-088d-4205-9ecc-92673a67e693")
    flow_forecaster.forecast()
