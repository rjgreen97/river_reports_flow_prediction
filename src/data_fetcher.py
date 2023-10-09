from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os


class DataFetcher:
    def __init__(self, site_id: str):
        self.site_id = site_id
        self.session = self._start_session()
        self.source_name = self.get_site_source_name()

    def generate_df(self) -> pd.DataFrame:
        self.result = self._get_site_flow_data()
        self.river_df = self._get_date_and_flow_data()
        self.session.close()
        return self.river_df

    def plot(self) -> None:
        plot_file_source_name = (
            self.source_name.lower().replace(" ", "_").replace(",", "")
        )
        plt = self.river_df.plot(x="ds", y="y", figsize=(12, 6), grid=True)
        plt.set_xlabel("Date")
        plt.set_ylabel("Flow (cfs)")
        plt.set_title(f"{self.source_name}")
        plt.figure.savefig(
            os.path.join(
                "plots", "historical_flow", f"{plot_file_source_name}_historical.png"
            )
        )
        self.session.close()

    def get_site_source_name(self) -> str:
        raw_sql = text(f"select * from rr.site where id = '{self.site_id}'")
        site_data = self.session.execute(raw_sql).fetchall()
        site_data_df = pd.DataFrame(site_data)
        self.session.close()
        return site_data_df["source_name"].values[0]

    def get_all_sites(self) -> list:
        raw_sql = text("select distinct site_id from rr.flow;")
        site_ids = self.session.execute(raw_sql).fetchall()
        site_ids_df = pd.DataFrame(site_ids)
        uuid_list = site_ids_df["site_id"].tolist()
        self.session.close()
        return [str(uuid_obj) for uuid_obj in uuid_list]

    def _start_session(self) -> sessionmaker:
        engine = create_engine("postgresql://rjgreen@localhost/riverreports")
        Session = sessionmaker(bind=engine)
        return Session()

    def _get_site_flow_data(self) -> list:
        raw_sql = text(
            f"select avg(value) as value, cast(ts as date) from rr.flow where site_id = \
            '{self.site_id}' group by cast(ts as date) order by ts asc"
        )
        return self.session.execute(raw_sql)

    def _get_date_and_flow_data(self) -> pd.DataFrame:
        df = pd.DataFrame(self.result.fetchall())
        y = df["value"]
        ds = df["ts"]
        river_df = pd.DataFrame({"ds": ds, "y": y})
        river_df["ds"] = pd.to_datetime(river_df["ds"], utc=True)
        river_df["ds"] = river_df["ds"].dt.strftime("%Y-%m-%d %H:%M:%S")
        river_df["ds"] = pd.to_datetime(river_df["ds"])
        river_df["y"] = river_df["y"].astype(float)
        river_df = river_df.drop_duplicates(subset="ds", keep="first")
        return river_df.reset_index(drop=True)


if __name__ == "__main__":
    data_fetcher = DataFetcher("901f7826-7cf2-44f9-833f-9cda40ebc374")
    df = data_fetcher.generate_df()
    data_fetcher.plot()
