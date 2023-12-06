from src.flow_site import FlowSite
from src.forecast import Forecast

import pandas as pd
import warnings

from statsmodels.tools.sm_exceptions import ConvergenceWarning, ValueWarning
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima


warnings.filterwarnings(
    "ignore", category=UserWarning, module="statsmodels.tsa.base.tsamod"
)
warnings.filterwarnings(
    "ignore", category=ConvergenceWarning, module="statsmodels.base.model"
)
warnings.filterwarnings("ignore", category=ValueWarning, module="statsmodels.tsa.base")


class Forecaster:
    def __init__(self, flow_site: FlowSite) -> None:
        self.flow_site = flow_site

    def generate_forecast(self) -> Forecast:
        forecast_df = self.arima()
        return Forecast(forecast_df, site_id=self.flow_site.id)

    def arima(self):
        self.flow_site.df["ds"] = pd.to_datetime(self.flow_site.df["ds"])
        self.flow_site.df.sort_values(by="ds", inplace=True)
        self.flow_site.df.set_index("ds", inplace=True)
        self.flow_site.df["y"] = self.flow_site.df["y"].fillna(0)

        num_periods = len(self.flow_site.df.index)
        self.flow_site.df.index = pd.date_range(
            start=self.flow_site.df.index.min(), periods=num_periods, freq="D"
        )

        arima_param_finder = auto_arima(
            self.flow_site.df["y"], seasonal=True, suppress_warnings=True
        )
        p, d, q = arima_param_finder.get_params()["order"]
        sarima = SARIMAX(self.flow_site.df["y"], order=(p, d, q), freq="D")

        results = sarima.fit()
        forecast = results.get_forecast(steps=7)
        forecast_values = forecast.predicted_mean
        forecast_values = forecast_values.to_frame()

        if self.flow_site.df["y"].iloc[-3:].sum() == 0:
            forecast_values["predicted_mean"] = 0
        return forecast_values
