from src.flow_site import FlowSite
from sqlalchemy.orm.session import Session as SQLAlchemySession
from sqlalchemy.engine.cursor import CursorResult as SQLAlchemyCursorResult
import pandas as pd


def test_init():
    flow_site = FlowSite.for_id("901f7826-7cf2-44f9-833f-9cda40ebc374")
    assert flow_site.id == "901f7826-7cf2-44f9-833f-9cda40ebc374"


def test_generate_df():
    flow_site = FlowSite.for_id("901f7826-7cf2-44f9-833f-9cda40ebc374")
    flow_site.load_data()
    assert flow_site.df.columns.tolist() == ["ds", "y"]
    assert flow_site.df.dtypes[0] == "datetime64[ns]"
    assert flow_site.df.dtypes[1] == "float64"


def test_start_session():
    flow_site = FlowSite.for_id("901f7826-7cf2-44f9-833f-9cda40ebc374")
    session = flow_site._start_session()
    assert isinstance(session, SQLAlchemySession)


def test_get_site_result():
    flow_site = FlowSite.for_id("901f7826-7cf2-44f9-833f-9cda40ebc374")
    result = flow_site._get_site_result()
    assert isinstance(result, SQLAlchemyCursorResult)
    df = pd.DataFrame(result.fetchall())
    assert df.columns.tolist() == ["value", "ts"]


def test_get_date_and_flow_data():
    flow_site = FlowSite.for_id("901f7826-7cf2-44f9-833f-9cda40ebc374")
    result = flow_site._get_site_result()
    df = flow_site._get_date_and_flow_data(result)
    assert df.columns.tolist() == ["ds", "y"]
    assert df.dtypes[0] == "datetime64[ns]"
    assert df.dtypes[1] == "float64"
