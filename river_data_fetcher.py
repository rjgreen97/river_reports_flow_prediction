from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os


class RiverDataFetcher:
    def __init__(self, site_id: str):
        self.site_id = site_id

    def generate_df(self) -> pd.DataFrame:
        self.session = self._start_session()
        self.result = self._get_site_flow_data()
        self.river_df = self._get_date_and_flow_data()
        self.session.close()
        return self.river_df

    def plot(self) -> None:
        source_name = self._get_site_source_name()
        plot_file_source_name = source_name.lower().replace(" ", "_").replace(",", "")
        plt = self.river_df.plot(x="ds", y="y", figsize=(12, 6), grid=True)
        plt.set_xlabel("Date")
        plt.set_ylabel("Flow (cfs)")
        plt.set_title(f"{source_name}")
        plt.figure.savefig(os.path.join("plots", f"{plot_file_source_name}_plot.png"))

    def _start_session(self) -> sessionmaker:
        engine = create_engine("postgresql://rjgreen@localhost/riverreports")
        Session = sessionmaker(bind=engine)
        return Session()

    def _get_site_flow_data(self) -> list:
        raw_sql = text(
            f"select * from rr.flow where site_id = '{self.site_id}' order by created_at desc"
        )
        return self.session.execute(raw_sql)

    def _get_date_and_flow_data(self) -> pd.DataFrame:
        df = pd.DataFrame(self.result.fetchall())
        y = df["value"]
        ds = df["created_at"]
        river_df = pd.DataFrame({"ds": ds, "y": y})
        river_df["ds"] = pd.to_datetime(river_df["ds"], utc=True)
        river_df["ds"] = river_df["ds"].dt.strftime("%Y-%m-%d %H:%M:%S")
        river_df["ds"] = pd.to_datetime(river_df["ds"])
        river_df["y"] = river_df["y"].astype(float)
        river_df = river_df.drop_duplicates(subset='ds', keep='first')
        return river_df.reset_index(drop=True)

    def _get_site_source_name(self) -> str:
        raw_sql = text(f"select * from rr.site where id = '{self.site_id}'")
        site_data = self.session.execute(raw_sql).fetchall()
        site_data_df = pd.DataFrame(site_data)
        return site_data_df["source_name"].values[0]


if __name__ == "__main__":
    river_data_fetcher = RiverDataFetcher("2813acc0-1dc3-413f-b27c-284e934732a2")
    df = river_data_fetcher.generate_df()
    river_data_fetcher.plot()
    print(df)
