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
                    print(f"Forecasting {site_id}")
                    forecaster = Forecaster(site_id)
                    forecast = forecaster.generate_forecast()
                    # forecast.save()
        except Exception as e:
            print(e)

    def _get_all_site_ids(self) -> list:
        Session = sessionmaker(
            bind=create_engine("postgresql://rjgreen@localhost/riverreports")
        )
        session = Session()
        site_ids = session.execute(
            text("select distinct site_id from rr.flow;")
        ).fetchall()
        site_ids_df = pd.DataFrame(site_ids)
        uuid_list = site_ids_df["site_id"].tolist()
        session.close()
        return [str(uuid_obj) for uuid_obj in uuid_list]

    def _get_excluded_sites(self):
        with open("excluded_sites.txt", "r") as f:
            excluded_sites_list = f.read().splitlines()
            return excluded_sites_list


if __name__ == "__main__":
    forecasting_session = ForecastingSession()
    forecasting_session.forecast_all_sites()
