# debug_env.py
from alembic.config import Config
from alembic import command

from src.settings import ROOT_FOLDER

# Path to alembic.ini
alembic_cfg = Config(str(ROOT_FOLDER / "alembic.ini"))

# Example: run upgrade head
command.upgrade(alembic_cfg, "head")