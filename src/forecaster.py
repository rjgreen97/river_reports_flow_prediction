from src.flow_site import FlowSite
from neuralprophet import NeuralProphet, df_utils
from src.forecast import Forecast
import torch
import time
import pandas as pd


class Forecaster:
    def __init__(self, flow_site: FlowSite) -> None:
        self.flow_site = flow_site
        self.device = "gpu" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

    def generate_forecast(self) -> Forecast:
        start_time = time.time()
        model = self._create_neural_prophet_model()
        self._add_custom_seasonalities(model)
        self._fit_model(model)
        df_future = self._create_future_dataframe(model)
        forecast_df = self._predict_future(model, df_future)
        end_time = time.time()
        print(f"Elapsed time: {((end_time - start_time) / 60):.2f} minutes\n")
        return Forecast(forecast_df, site_id=self.flow_site.id)

    def _create_neural_prophet_model(self) -> NeuralProphet:
        return NeuralProphet(
            weekly_seasonality="auto",
            daily_seasonality="auto",
            accelerator=self.device,
            batch_size=8,
        )

    def _add_custom_seasonalities(self, model: NeuralProphet) -> None:
        seasons = ["summer", "fall", "winter", "spring"]
        for season in seasons:
            model.add_seasonality(
                name=f"weekly_{season}",
                period=7,
                fourier_order=3,
                condition_name=season,
            )

    def _fit_model(self, model: NeuralProphet) -> None:
        print(f"Predicting for Site ID: {self.flow_site.id}")
        model.fit(
            self.flow_site.df,
            freq="D",
            epochs=1000,
            metrics=["MSE"],
            early_stopping=False,
        )

    def _create_future_dataframe(self, model) -> pd.DataFrame:
        df_future = model.make_future_dataframe(
            self.flow_site.df, n_historic_predictions=False, periods=7
        )
        return df_utils.add_quarter_condition(df_future)

    def _predict_future(
        self, model: NeuralProphet, df_future: pd.DataFrame
    ) -> pd.DataFrame:
        return model.predict(df_future)
