from src.forecaster import Forecaster
from src.data_fetcher import DataFetcher

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

class ForecastingSession:
    def __init__(self):
        pass

    def get_all_site_ids(self) -> list:
        engine = create_engine("postgresql://rjgreen@localhost/riverreports")
        Session = sessionmaker(bind=engine)
        session = Session()
        raw_sql = text("select distinct site_id from rr.flow;")
        site_ids = session.execute(raw_sql).fetchall()
        site_ids_df = pd.DataFrame(site_ids)
        uuid_list = site_ids_df['site_id'].tolist()
        session.close()
        return [str(uuid_obj) for uuid_obj in uuid_list]


if __name__ == "__main__":
   forecasting_session = ForecastingSession()
   site_ids = forecasting_session.get_all_site_ids() 
   print(len(site_ids))
