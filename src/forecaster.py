from src.data_fetcher import DataFetcher
from neuralprophet import NeuralProphet, set_log_level
import pandas as pd
import os

set_log_level("ERROR")


class Forecaster:
    def __init__(self, site_id: str) -> None:
        self.data_fetcher = DataFetcher(site_id)
        self.model = NeuralProphet()

    def forecast(self) -> None:
        df = self._get_df()
        print(df)
        source_name = self._get_site_source_name()
        self.model.fit(df, freq="H")
        df_future = self.model.make_future_dataframe(
            df, n_historic_predictions=True, periods=365
        )
        forecast_df = self.model.predict(df_future)
        forecast_df.to_csv(
            os.path.join("data", "forecasted_flow", f"{source_name}_forecast.csv")
        )

        plot = self.model.plot(forecast_df)
        plot.write_image(
            os.path.join(
                "data", "forecasted_flow_plots", f"{source_name}_forecast.png"
            )
        )

    def _get_df(self) -> pd.DataFrame:
        return self.data_fetcher.generate_df()

    def _get_site_source_name(self) -> str:
        return self.data_fetcher.source_name.lower().replace(" ", "_").replace(",", "")

if __name__ == "__main__":
    forecaster = Forecaster("91b65ab1-7509-450b-8910-30a1e9227cc4")
    forecaster.forecast()
