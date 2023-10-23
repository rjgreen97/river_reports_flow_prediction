from src.forecasting_session import ForecastingSession
from src.data_fetcher import DataFetcher


def test_init():
    forecasting_session = ForecastingSession()
    assert isinstance(forecasting_session.site_ids_list, list)
    assert len(forecasting_session.site_ids_list) > 0
    assert isinstance(forecasting_session.database_url, str)


def test_get_all_site_ids():
    forecasting_session = ForecastingSession()
    site_ids = forecasting_session._get_all_site_ids()
    assert isinstance(site_ids, list)
    assert len(site_ids) == 545
    assert isinstance(site_ids[0], str)


def test_get_excluded_sites():
    forecasting_session = ForecastingSession()
    excluded_sites = forecasting_session._get_excluded_sites()
    assert isinstance(excluded_sites, list)
    assert isinstance(excluded_sites[0], str)
