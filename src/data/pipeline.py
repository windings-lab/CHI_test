import json
from datetime import date

from ..http_client import client
from ..settings import RAW_DATA_FOLDER, API_URL
from ..util import ensure_folder


class DataPipeline:
    def acquire(self):
        geo_data = self._load_geolocation()
        geo_data = geo_data[0]
        lat, lon = geo_data["lat"], geo_data["lon"]
        city_forecast_data = self._load_forecast(lat, lon)

        response_file = self._get_raw_data_folder() / "response.json"
        response_file.write_text(json.dumps(city_forecast_data, indent=4))

        return city_forecast_data

    def _load_geolocation(self, city: str = "Kyiv"):
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

    def _get_raw_data_folder(self):
        today = date.today().isoformat()
        return ensure_folder(RAW_DATA_FOLDER / today)
