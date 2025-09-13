import json
from datetime import date

from src.city import City
from src.http_client import client
from src.settings import RAW_DATA_FOLDER, URL
from src.util import ensure_folder


class Pipeline:
    async def acquire(self):
        geo_data = await self._load_geolocation()
        city = City.from_dict(geo_data[0])
        city_forecast_data = await self._load_forecast(city)
        response_file = self._get_raw_data_folder() / "response.json"
        response_file.write_text(json.dumps(city_forecast_data, indent=4))

    async def _load_geolocation(self, city: str = "Kyiv"):
        url = f"{URL}/geo/1.0/direct"
        params = {
            "q": city,
        }
        async with client() as cl:
            response = await cl.get(url, params=params)

        return response.json()

    async def _load_forecast(self, city: City):
        url = f"{URL}/data/2.5/forecast"
        params = {
            "lat": city.lat,
            "lon": city.lon,
            "cnt": 5,
            "units": "metric",
        }
        async with client() as cl:
            response = await cl.get(url, params=params)

        return response.json()

    def _get_raw_data_folder(self):
        today = date.today().isoformat()
        return ensure_folder(RAW_DATA_FOLDER / today)
