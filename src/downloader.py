import requests
import os
import datetime


class Downloader:
    def __init__(self, site_id, num_days=7):
        self.site_id = site_id
        self.num_days = num_days

    def fetch_and_save_flow_data(self):
        url = self.create_url()
        response = self.make_request(url)
        filename = self.generate_filename(response.status_code)
        site_name = self.get_site_name(url)
        self.save_file(filename, response)

    def create_url(self):
        today = datetime.datetime.now()
        past = datetime.timedelta(days=-self.num_days)
        begin_date = (today + past).strftime("%Y-%m-%d")
        end_date = today.strftime("%Y-%m-%d")
        return f"https://waterservices.usgs.gov/nwis/iv/?format=json&sites={self.site_id}&startDT={begin_date}&endDT={end_date}&parameterCd=00060,00010&siteType=ST&siteStatus=all"

    def make_request(self, url):
        response = requests.get(url)
        return response

    def generate_filename(self, status_code):
        if status_code == 200:
            return f"{self.site_id}.csv"
        else:
            return f"{self.site_id}.html"

    def get_site_name(self, url):
        response = requests.get(url)
        return response.json()["value"]["timeSeries"][0]["sourceInfo"]["siteName"]

    def save_file(self, filename, response):
        os.makedirs("tmp_data", exist_ok=True)
        with open(os.path.join("tmp_data", filename), "w") as f:
            f.write("date,flow\n")
            for item in response.json()["value"]["timeSeries"][0]["values"][0]["value"]:
                parsed_line = f"{item['dateTime']},{float(item['value'])}\n"
                f.write(parsed_line)


if __name__ == "__main__":
    downloader = Downloader("09057500")
    downloader.fetch_and_save_flow_data()
