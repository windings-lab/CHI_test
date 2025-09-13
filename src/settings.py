import os
from pathlib import Path

from src.util import ensure_folder


ROOT_FOLDER = Path(__file__).parent.parent
CACHE_FOLDER = ensure_folder(ROOT_FOLDER / Path("cache"))
DATA_FOLDER = ROOT_FOLDER / Path("data")
RAW_DATA_FOLDER = DATA_FOLDER / Path("raw")

API_KEY = os.getenv("API_KEY")
URL = r"https://api.openweathermap.org"
