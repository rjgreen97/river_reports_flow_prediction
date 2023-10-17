from src.data_fetcher import DataFetcher
from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import os
from src.forecast import Forecast

set_log_level("ERROR")


class Forecaster:
    def __init__(self, site_id: str) -> None:
        self.site_id = site_id
        self.data_fetcher = DataFetcher(self.site_id)
        self.model = NeuralProphet()

    def generate_forecast(self) -> Forecast:
        df = self._get_df()
        source_name = self._get_site_source_name()
        self.model.fit(df, freq="H")
        df_future = self.model.make_future_dataframe(
            df, n_historic_predictions=True, periods=365
        )
        forecast_df = self.model.predict(df_future)
        self._plot_forecast(forecast_df, source_name)
        return Forecast(forecast_df, site_id=self.site_id)

    def _plot_forecast(self, forecast_df: pd.DataFrame, source_name: str) -> None:
        plot = self.model.plot(forecast_df)
        plot.write_image(
            os.path.join("data", "forecasted_flow_plots", f"{source_name}_forecast.png")
        )

    def _get_df(self) -> pd.DataFrame:
        return self.data_fetcher.generate_df()

    def _get_site_source_name(self) -> str:
        return self.data_fetcher.source_name.lower().replace(" ", "_").replace(",", "")


if __name__ == "__main__":
    forecaster = Forecaster("91b65ab1-7509-450b-8910-30a1e9227cc4")
    forecaster.generate_forecast()
