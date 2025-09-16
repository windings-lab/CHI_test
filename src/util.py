from datetime import date
from pathlib import Path


def ensure_folder(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    return path

def create_folder_and_append_today(path: Path):
    today = date.today().isoformat()
    return ensure_folder(path / today)