import sqlalchemy
import os
from src.forecast_parser import ForecastParser

class DatabaseWriter:
    def __init__(self):
        self.engine = sqlalchemy.create_engine("postgresql://rjgreen@localhost/riverreports")

    def write_forecast_data(self):
        csv_filepaths = self._get_all_csv_filepaths()
        for csv_filepath in csv_filepaths:
            forecast_df = ForecastParser().parse_forecast(csv_filepath)
            forecast_df.to_sql("forecast", self.engine, if_exists="replace", index=False)

    def _get_all_csv_filepaths(self):
        csv_filepaths = []
        for root, _dirs, files in os.walk(os.path.join("data", "forecasted_flow")):
            for file in files:
                if file.endswith(".csv"):
                    csv_filepaths.append(os.path.join(root, file))
        return csv_filepaths


if __name__ == "__main__":
    database_writer = DatabaseWriter()
    database_writer.write_forecast_data()
