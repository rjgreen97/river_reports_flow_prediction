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
                if not (
                    site_id == "81b4b099-088d-4205-9ecc-92673a67e693"
                    or site_id == "8eeffcda-9313-4178-ac91-57e331d081ec"
                    or site_id == "901f7826-7cf2-44f9-833f-9cda40ebc374"
                ):
                    flow_forecaster = Forecaster(site_id)
                    flow_forecaster.forecast()
        except Exception as e:
            print(e)

    def _get_all_site_ids(self) -> list:
        engine = create_engine("postgresql://rjgreen@localhost/riverreports")
        Session = sessionmaker(bind=engine)
        session = Session()
        raw_sql = text("select distinct site_id from rr.flow;")
        site_ids = session.execute(raw_sql).fetchall()
        site_ids_df = pd.DataFrame(site_ids)
        uuid_list = site_ids_df["site_id"].tolist()
        session.close()
        return [str(uuid_obj) for uuid_obj in uuid_list]


if __name__ == "__main__":
    forecasting_session = ForecastingSession()
    forecasting_session.forecast_all_sites()
