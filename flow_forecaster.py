from river_data_fetcher import RiverDataFetcher
from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import os

set_log_level("ERROR")


class FlowForecaster:
    def __init__(self, site_id: str):
        self.site_id = site_id
        self.model = NeuralProphet()
        self.df = self._get_df()
        self.source_name = self._get_site_source_name()

    def forecast(self) -> None:
        self.train()
        df_future = self.model.make_future_dataframe(self.df, n_historic_predictions=True, periods=365)
        forecast = self.model.predict(df_future)
        plot = self.model.plot(forecast)
        plot.write_image(os.path.join("plots", "forecasted_flow", f"{self.source_name}_forecast.png"))

    def train(self) -> None:
        self.model.fit(self.df, freq="H")

    def _get_df(self) -> pd.DataFrame:
        river_data_fetcher = RiverDataFetcher(self.site_id)
        return river_data_fetcher.generate_df()

    def _get_site_source_name(self) -> str:
        river_data_fetcher = RiverDataFetcher(self.site_id)
        return river_data_fetcher.source_name.lower().replace(" ", "_").replace(",", "")


if __name__ == "__main__":
    flow_forecaster = FlowForecaster("03a427ca-f37e-4232-8144-3d33f2aeb0c5")
    flow_forecaster.forecast()
