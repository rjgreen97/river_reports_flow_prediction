from sqlalchemy import text
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


class FlowSite:
    @classmethod
    def for_id(cls, site_id: str, session) -> str:
        flow_site = cls(site_id, session)
        flow_site.load_data()
        return flow_site

    def __init__(self, id: str, session):
        self.id = id
        self.session = session

    def load_data(self) -> None:
        result = self._get_site_result()
        self.df = self._get_date_and_flow_data(result)
        self.session.close()

    def _get_site_result(self) -> list:
        raw_sql = text(
            f"SELECT AVG(value) AS value, CAST(ts AS DATE) FROM rr.flow WHERE site_id = '{self.id}' GROUP BY CAST(ts AS DATE) ORDER BY ts ASC"
        )
        return self.session.execute(raw_sql)

    def _get_date_and_flow_data(self, result) -> pd.DataFrame:
        df = pd.DataFrame(result.fetchall())
        if df.empty:
            return df
        else:
            y = df["value"]
            ds = df["ts"]
            river_df = pd.DataFrame({"ds": ds, "y": y})
            river_df["ds"] = pd.to_datetime(river_df["ds"], utc=True)
            river_df["ds"] = river_df["ds"].dt.strftime("%Y-%m-%d %H:%M:%S")
            river_df["ds"] = pd.to_datetime(river_df["ds"])
            river_df["y"] = river_df["y"].astype(float)
            river_df = river_df.drop_duplicates(subset="ds", keep="first")
            return river_df.reset_index(drop=True)
