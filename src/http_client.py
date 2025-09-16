from pathlib import Path

import hishel
import httpx

from src.settings import ROOT_FOLDER, API_URL, API_KEY

storage = hishel.FileStorage(
    serializer=hishel.JSONSerializer(),
    base_path=ROOT_FOLDER / Path("cache"),
    ttl=3600 * 24,
)

controller = hishel.Controller(force_cache=True)

cache_transport = hishel.CacheTransport(transport=httpx.HTTPTransport(), storage=storage, controller=controller)

def client() -> httpx.Client:
    return httpx.Client(
        base_url=API_URL,
        transport=cache_transport,
        params={"appid": API_KEY}
    )
