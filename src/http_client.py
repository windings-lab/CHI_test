from pathlib import Path

import hishel
import httpx

from settings import ROOT_FOLDER, URL, API_KEY

storage = hishel.AsyncFileStorage(
    serializer=hishel.JSONSerializer(),
    base_path=ROOT_FOLDER / Path("cache"),
    ttl=3600 * 24,
)

controller = hishel.Controller(force_cache=True)

cache_transport = hishel.AsyncCacheTransport(transport=httpx.AsyncHTTPTransport(), storage=storage, controller=controller)

def client() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url=URL,
        transport=cache_transport,
        params={"appid": API_KEY}
    )
