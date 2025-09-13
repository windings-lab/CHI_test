from pathlib import Path

import hishel
import httpx

from settings import root_folder


cache_folder = root_folder / Path("cache")
cache_folder.mkdir(parents=True, exist_ok=True)
storage = hishel.AsyncFileStorage(serializer=hishel.JSONSerializer(), base_path=root_folder / Path("cache"))

controller = hishel.Controller(force_cache=True)

cache_transport = hishel.AsyncCacheTransport(transport=httpx.AsyncHTTPTransport(), storage=storage, controller=controller)
client = httpx.AsyncClient(transport=cache_transport)
