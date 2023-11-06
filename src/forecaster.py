from src.flow_site import FlowSite
from neuralprophet import NeuralProphet, set_log_level
from src.forecast import Forecast

set_log_level("ERROR")


class Forecaster:
    def __init__(self, flow_site: FlowSite) -> None:
        self.flow_site = flow_site

    def generate_forecast(self) -> Forecast:
        model = NeuralProphet()
        print(f"Predicting for Site ID: {self.flow_site.id}")
        model.fit(
            self.flow_site.df,
            freq="D",
            early_stopping=False,
            epochs=250,
            metrics=["MSE"],
        )
        df_future = model.make_future_dataframe(
            self.flow_site.df, n_historic_predictions=False, periods=7
        )
        forecast_df = model.predict(df_future)
        return Forecast(forecast_df, site_id=self.flow_site.id)
