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
        result = self._get_site_result()
        river_df = self._get_date_and_flow_data(result)
        self.session.close()
        return river_df

    def plot_historical_flows(self) -> None:
        river_df = self.generate_df()
        plot_file_source_name = (
            self.source_name.lower().replace(" ", "_").replace(",", "")
        )
        plt = river_df.plot(x="ds", y="y", figsize=(12, 6), grid=True)
        plt.set_xlabel("Date")
        plt.set_ylabel("Flow (cfs)")
        plt.set_title(f"{self.source_name}")
        plt.figure.savefig(
            os.path.join(
                "data",
                "historical_flow_plots",
                f"{plot_file_source_name}_historical.png",
            )
        )
        self.session.close()

    def get_site_source_name(self) -> str:
        raw_sql = text(f"select * from rr.site where id = '{self.site_id}'")
        site_data = self.session.execute(raw_sql).fetchall()
        site_data_df = pd.DataFrame(site_data)
        self.session.close()
        return site_data_df["source_name"].values[0]

    def _start_session(self) -> sessionmaker:
        engine = create_engine("postgresql://rjgreen@localhost/riverreports")
        Session = sessionmaker(bind=engine)
        return Session()

    def _get_site_result(self) -> list:
        raw_sql = text(
            f"select avg(value) as value, cast(ts as date) from rr.flow where site_id = \
            '{self.site_id}' group by cast(ts as date) order by ts asc"
        )
        return self.session.execute(raw_sql)

    def _get_date_and_flow_data(self, result) -> pd.DataFrame:
        df = pd.DataFrame(result.fetchall())
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
    data_fetcher.plot_historical_flows()
