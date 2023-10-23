# from src.data_fetcher import DataFetcher
# import os
# from sqlalchemy.orm.session import Session as SQLAlchemySession
# from sqlalchemy.engine.cursor import CursorResult as SQLAlchemyCursorResult
# import pandas as pd


# def test_init():
#     data_fetcher = DataFetcher("901f7826-7cf2-44f9-833f-9cda40ebc374")
#     assert data_fetcher.site_id == "901f7826-7cf2-44f9-833f-9cda40ebc374"
#     assert data_fetcher.source_name == "Stones River below J Percy Priest Dam"


# def test_generate_df():
#     data_fetcher = DataFetcher("901f7826-7cf2-44f9-833f-9cda40ebc374")
#     df = data_fetcher.generate_df()
#     assert df.columns.tolist() == ["ds", "y"]
#     assert df.dtypes[0] == "datetime64[ns]"
#     assert df.dtypes[1] == "float64"


# def plot_historical_flows():
#     data_fetcher = DataFetcher("901f7826-7cf2-44f9-833f-9cda40ebc374")
#     data_fetcher.plot()
#     assert os.path.exists(
#         "data/historical_flow_plots/stones_river_below_j_percy_priest_dam_historical.png"
#     )


# def test_get_site_source_name():
#     data_fetcher = DataFetcher("901f7826-7cf2-44f9-833f-9cda40ebc374")
#     source_name = data_fetcher.get_site_source_name()
#     assert source_name == "Stones River below J Percy Priest Dam"

# def test_get_database_url():
#     data_fetcher = DataFetcher("901f7826-7cf2-44f9-833f-9cda40ebc374")
#     connection_string = data_fetcher.get_database_url()
#     assert connection_string == "postgresql://rjgreen@localhost/riverreports"

# def test_start_session():
#     data_fetcher = DataFetcher("901f7826-7cf2-44f9-833f-9cda40ebc374")
#     session = data_fetcher._start_session()
#     assert isinstance(session, SQLAlchemySession)


# def test_get_site_result():
#     data_fetcher = DataFetcher("901f7826-7cf2-44f9-833f-9cda40ebc374")
#     result = data_fetcher._get_site_result()
#     assert isinstance(result, SQLAlchemyCursorResult)
#     df = pd.DataFrame(result.fetchall())
#     assert df.columns.tolist() == ["value", "ts"]


# def test_get_date_and_flow_data():
#     data_fetcher = DataFetcher("901f7826-7cf2-44f9-833f-9cda40ebc374")
#     result = data_fetcher._get_site_result()
#     df = data_fetcher._get_date_and_flow_data(result)
#     assert df.columns.tolist() == ["ds", "y"]
#     assert df.dtypes[0] == "datetime64[ns]"
#     assert df.dtypes[1] == "float64"
