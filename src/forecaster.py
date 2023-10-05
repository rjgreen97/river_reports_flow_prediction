from src.data_fetcher import DataFetcher
from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import os

set_log_level("ERROR")


class Forecaster:
    def __init__(self, site_id: str):
        self.data_fetcher = DataFetcher(site_id)
        self.model = NeuralProphet()
        self.df = self._get_df()
        self.source_name = self._get_site_source_name()

    def forecast(self) -> None:
        self.model.fit(self.df, freq="H")
        df_future = self.model.make_future_dataframe(self.df, n_historic_predictions=True, periods=365)
        forecast = self.model.predict(df_future)
        plot = self.model.plot(forecast)
        plot.write_image(os.path.join("plots", "forecasted_flow", f"{self.source_name}_forecast.png"))

    def _get_df(self) -> pd.DataFrame:
        return self.data_fetcher.generate_df()

    def _get_site_source_name(self) -> str:
        return self.data_fetcher.source_name.lower().replace(" ", "_").replace(",", "")

if __name__ == "__main__":
    flow_forecaster = Forecaster("fa5ee27c-60bc-4801-ab60-7ab532734fa8")
    flow_forecaster.forecast()
