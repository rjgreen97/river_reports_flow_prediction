from src.flow_site import FlowSite
from src.forecast import Forecast

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import itertools


class Forecaster:
    def __init__(self, flow_site: FlowSite) -> None:
        self.flow_site = flow_site

    def generate_forecast(self) -> Forecast:
        forecast_df = self.arima()
        return Forecast(forecast_df, site_id=self.flow_site.id)

    def arima(self):
        print(f"Forecasting site: {self.flow_site.id}")
        self.flow_site.df["ds"] = pd.to_datetime(self.flow_site.df["ds"])
        self.flow_site.df.sort_values(by="ds", inplace=True)
        self.flow_site.df.set_index("ds", inplace=True)

        num_periods = len(self.flow_site.df.index)
        self.flow_site.df.index = pd.date_range(
            start=self.flow_site.df.index.min(), periods=num_periods, freq="H"
        )

        p_values = range(0, 5)
        d_values = range(0, 2)
        q_values = range(0, 5)

        best_aic = float("inf")
        best_params = None

        for p, d, q in itertools.product(p_values, d_values, q_values):
            try:
                model = SARIMAX(
                    self.flow_site.df["y"],
                    order=(p, d, q),
                    freq="H",
                    enforce_stationarity=True,
                )
                results = model.fit(maxiter=1000)

                current_aic = results.aic

                if current_aic < best_aic:
                    best_aic = current_aic
                    best_params = (p, d, q)

            except Exception as e:
                print(f"Error for p={p}, d={d}, q={q}: {e}")

        p, d, q = best_params


        print(f"Running ARIMA with p={p}, d={d}, q={q}")
        arima = SARIMAX(
            self.flow_site.df["y"],
            order=(p, d, q),
            freq="H",
            enforce_stationarity=False,
        )

        results = arima.fit(maxiter=1000)
        forecast = results.get_forecast(steps=72)
        forecast_values = forecast.predicted_mean
        forecast_values = forecast_values.to_frame()

        if self.flow_site.df["y"].iloc[-3:].sum() == 0:
            forecast_values["predicted_mean"] = 0
        return forecast_values
