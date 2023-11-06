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
        self.db_session = self._create_db_session()
        self.site_ids_list = self._get_all_site_ids()

    def forecast_all_sites(self) -> None:
        excluded_sites = self._get_excluded_sites()
        try:
            for site_id in self.site_ids_list:
                if site_id not in excluded_sites:
                    flow_site = FlowSite.for_id(site_id, self.db_session)
                    forecaster = Forecaster(flow_site)
                    forecast = forecaster.generate_forecast()
                    forecast.save()
        except psycopg2.Error as e:
            print(f"Error forecasting site {site_id}: {e}")

    def _get_all_site_ids(self) -> list:
        site_ids = self.db_session.execute(
            text("SELECT DISTINCT id FROM rr.site WHERE show = TRUE;")
        ).fetchall()
        site_ids_df = pd.DataFrame(site_ids)
        uuid_list = site_ids_df["id"].tolist()
        self.db_session.close()
        return [str(uuid_obj) for uuid_obj in uuid_list]

    def _get_excluded_sites(self) -> list:
        with open("excluded_sites.txt", "r") as f:
            excluded_sites_list = f.read().splitlines()
            return excluded_sites_list

    def _create_db_session(self) -> sessionmaker:
        engine = create_engine(os.getenv("DATABASE_URL"))
        Session = sessionmaker(bind=engine)
        return Session()


if __name__ == "__main__":
    forecasting_session = ForecastingSession()
    forecasting_session.forecast_all_sites()
