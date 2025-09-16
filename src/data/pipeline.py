import json
import pandas as pd

from sqlalchemy import select, func

from settings import REPORT_FOLDER
from ..http_client import client
from ..settings import RAW_DATA_FOLDER, API_URL, PROCESSED_DATA_FOLDER
from ..util import create_folder_and_append_today
from ..db import engine, session, Forecast


class DataPipeline:
    def acquire(self, city: str = "Kyiv"):
        geo_data = self._load_geolocation(city)
        geo_data = geo_data[0]
        lat, lon = geo_data["lat"], geo_data["lon"]
        city_forecast_data = self._load_forecast(lat, lon)

        response_file = create_folder_and_append_today(RAW_DATA_FOLDER) / f"{city.lower()}_response.json"
        response_file.write_text(json.dumps(city_forecast_data, indent=4))

        return city_forecast_data

    def process(self, raw_data: dict):
        list_of_forecasts = raw_data["list"]
        city = raw_data["city"]["name"]

        if city == 'Pushcha-Vodytsya':
            city = 'Kyiv'

        result = []

        for forecast in list_of_forecasts:
            main: dict = forecast["main"]
            del main["feels_like"]
            del main["temp_min"]
            del main["temp_max"]
            del main["temp_kf"]
            main["date"] = forecast["dt"]
            main["temperature"] = main.pop("temp")
            main["ground_level"] = main.pop("grnd_level")
            main["city"] = city

            result.append(main)

        data_file = create_folder_and_append_today(PROCESSED_DATA_FOLDER) / "data.parquet"
        df = pd.DataFrame(result)

        cols = ["city", "date"] + [c for c in df.columns if c not in ["city", "date"]]
        df = df[cols]
        df["date"] = pd.to_datetime(df["date"], unit="s")

        if data_file.exists():
            df_existing = pd.read_parquet(data_file)
            df_merged = pd.concat([df_existing, df], ignore_index=True)
            df_merged.drop_duplicates(subset=["city", "date"], inplace=True)
            df = df_merged

        df.to_parquet(data_file)

        return df

    def save_to_database(self, df: pd.DataFrame):
        df.to_sql(
            "forecast",
            con=engine,
            if_exists="replace",
        )

    def analyze(self):
        # --- 1. Average temperature overall ---
        avg_temp = session.execute(
            select(func.avg(Forecast.temperature))
        ).scalar_one()

        # --- 2. Count of unique cities ---
        unique_cities = session.execute(
            select(func.count(func.distinct(Forecast.city)))
        ).scalar_one()

        # --- 3. Average temperature per city ---
        stmt = select(
            Forecast.city,
            func.avg(Forecast.temperature).label("avg_temp")
        ).group_by(Forecast.city)

        avg_per_city = {city: round(temp, 2) for city, temp in session.execute(stmt).all()}

        # --- Save all results to a dictionary ---
        results_dict = {
            "average_temperature_overall": round(avg_temp, 2),
            "unique_cities_count": unique_cities,
            "average_temperature_per_city": avg_per_city
        }

        report_file = create_folder_and_append_today(REPORT_FOLDER) / "report.json"

        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(results_dict, f, indent=4)

    def _load_geolocation(self, city):
        url = f"{API_URL}/geo/1.0/direct"
        params = {
            "q": city,
        }
        with client() as cl:
            response = cl.get(url, params=params)

        return response.json()

    def _load_forecast(self, lat: float, lon: float):
        url = f"{API_URL}/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "cnt": 5,
            "units": "metric",
        }
        with client() as cl:
            response = cl.get(url, params=params)

        return response.json()
