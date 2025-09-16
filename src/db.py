from datetime import datetime

from sqlalchemy import create_engine, String, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, sessionmaker
from sqlalchemy.orm import mapped_column

from src.settings import (
    ROOT_FOLDER, 
    DATABASE_TYPE, 
    POSTGRES_HOST, 
    POSTGRES_PORT, 
    POSTGRES_DB, 
    POSTGRES_USER, 
    POSTGRES_PASSWORD
)

Base = declarative_base()

class Forecast(Base):
    __tablename__ = 'forecast'

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(40))
    date: Mapped[datetime] = mapped_column(DateTime)
    temperature: Mapped[float] = mapped_column(Float)
    pressure: Mapped[int] = mapped_column(Integer)
    sea_level: Mapped[int] = mapped_column(Integer)
    humidity: Mapped[int] = mapped_column(Integer)
    ground_level: Mapped[int] = mapped_column(Integer)

# Create database URL based on database type
def get_database_url():
    if DATABASE_TYPE == "postgres":
        return f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    else:
        return f'sqlite:///{ROOT_FOLDER / "data.db"}'

# Create an engine and a session
engine = create_engine(get_database_url())
Session = sessionmaker(bind=engine)
session = Session()