from river_data_fetcher import RiverDataFetcher
from neuralprophet import NeuralProphet, set_log_level
import pandas as pd

set_log_level("ERROR")


class FlowForecaster:
    def __init__(self, site_id: str):
        self.site_id = site_id
        self.df = self._get_df()
        self.model = NeuralProphet()

    def forecast(self):
        df_future = self.model.make_future_dataframe(self.df, n_historic_predictions=True, periods=365)
        forecast = self.model.predict(df_future)

    def train(self):
        self.model.fit(self.df, freq="H")

    def _get_df(self) -> pd.DataFrame:
        river_data_fetcher = RiverDataFetcher(self.site_id)
        return river_data_fetcher.generate_df()


if __name__ == "__main__":
    flow_forecaster = FlowForecaster("2813acc0-1dc3-413f-b27c-284e934732a2")
    print(flow_forecaster.df.head())
