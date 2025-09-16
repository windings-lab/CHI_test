from datetime import datetime

from sqlalchemy import create_engine, String, DateTime, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from settings import ROOT_FOLDER

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

# Create an engine and a session
engine = create_engine(f'sqlite:///{ROOT_FOLDER / "data.db"}')