import asyncio
import json

from http_client import client
from settings import API_KEY

URL = r"https://api.openweathermap.org"


async def load_data():
    url = f"{URL}/geo/1.0/direct"
    params = {
        "q": "Kyiv",
        "appid": API_KEY
    }
    async with client as cl:
        response = await cl.get(url, params=params)

    return response.json()

async def main():
    data = await load_data()
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
