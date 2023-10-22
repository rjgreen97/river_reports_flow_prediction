from src.forecaster import Forecaster

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class ForecastingSession:
    def __init__(self):
        self.site_ids_list = self._get_all_site_ids()

    def forecast_all_sites(self) -> None:
        try:
            for site_id in self.site_ids_list:
                if not (site_id in self._get_excluded_sites()):
                    forecaster = Forecaster(site_id)
                    forecast = forecaster.generate_forecast()
                    forecast.save()
        except Exception as e:
            print(f"Error forecasting site {site_id}: {e}")

    def _get_all_site_ids(self) -> list:
        Session = sessionmaker(
            bind=create_engine("postgresql://rjgreen@localhost/riverreports")
        )
        session = Session()
        site_ids = session.execute(
            text("select distinct id from rr.site where show = True;")
        ).fetchall()
        site_ids_df = pd.DataFrame(site_ids)
        uuid_list = site_ids_df["id"].tolist()
        session.close()
        return [str(uuid_obj) for uuid_obj in uuid_list]

    def _get_excluded_sites(self):
        with open("excluded_sites.txt", "r") as f:
            excluded_sites_list = f.read().splitlines()
            return excluded_sites_list


if __name__ == "__main__":
    forecasting_session = ForecastingSession()
    forecasting_session.forecast_all_sites()
