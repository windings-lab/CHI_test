import os
from pathlib import Path
from dotenv import load_dotenv

from src.util import ensure_folder

# Load environment variables from .env file
ROOT_FOLDER = Path(__file__).parent.parent
if not load_dotenv(ROOT_FOLDER / ".env"):
    print("No .env file found, using default values")

CACHE_FOLDER = ensure_folder(ROOT_FOLDER / Path("cache"))
DATA_FOLDER = ROOT_FOLDER / Path("data")

RAW_DATA_FOLDER = DATA_FOLDER / Path("raw")
PROCESSED_DATA_FOLDER = DATA_FOLDER / Path("processed")
REPORT_FOLDER = DATA_FOLDER / Path("reports")

API_KEY = os.getenv("API_KEY")
API_URL = r"https://api.openweathermap.org"

# Database configuration
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")  # sqlite or postgres
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "gaster")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")