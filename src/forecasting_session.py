from src.forecaster import Forecaster
from src.flow_site import FlowSite

import psycopg2
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


class ForecastingSession:
    def __init__(self):
        self.site_ids_list = self._get_all_site_ids()

    def forecast_all_sites(self) -> None:
        excluded_sites = self._get_excluded_sites()
        try:
            for site_id in self.site_ids_list:
                if site_id not in excluded_sites:
                    flow_site = FlowSite.for_id(site_id)
                    forecaster = Forecaster(flow_site)
                    forecast = forecaster.generate_forecast()
                    forecast.save()
        except psycopg2.Error as e:
            print(f"Error forecasting site {site_id}: {e}")

    def _get_all_site_ids(self) -> list:
        Session = sessionmaker(bind=create_engine(os.getenv("DATABASE_URL")))
        session = Session()
        site_ids = session.execute(
            text("SELECT DISTINCT id FROM rr.site WHERE show = TRUE;")
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
