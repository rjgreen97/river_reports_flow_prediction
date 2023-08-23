
import datetime

from src.usgs_downloader import USGSDownloader

def test_init():
    downloader = USGSDownloader("09057500")
    assert downloader.site_id == "09057500"
    assert downloader.num_days == 7

def test_create_url():
    num_days = 7
    downloader = USGSDownloader("09057500", num_days)
    url = downloader.create_url()
    today = datetime.datetime.now()
    past = datetime.timedelta(days=-num_days)
    test_begin_date = (today + past).strftime("%Y-%m-%d")
    test_end_date = today.strftime("%Y-%m-%d")
    assert url == f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites=09057500&startDT={test_begin_date}&endDT={test_end_date}&parameterCd=00060,00010&siteType=ST&siteStatus=all"

def test_make_request():
    downloader = USGSDownloader("09057500")
    url = downloader.create_url()
    response = downloader.make_request(url)
    assert response.status_code == 200

def test_generate_filename():
    downloader = USGSDownloader("09057500")
    url = downloader.create_url()
    response = downloader.make_request(url)
    filename = downloader.generate_filename(response.status_code)
    assert filename == "09057500.csv"

def test_get_site_name():
    downloader = USGSDownloader("09057500")
    url = downloader.create_url()
    site_name = downloader.get_site_name(url)
    assert site_name == "BLUE RIVER BELOW GREEN MOUNTAIN RESERVOIR, CO"
