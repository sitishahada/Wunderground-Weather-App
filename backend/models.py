# === backend/models.py ===
from sqlalchemy import Column, Integer, Float, String, Date, Time
from backend.database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    temperature = Column(Float)
    dew_point = Column(Float)
    humidity = Column(Float)
    wind = Column(String)
    wind_speed = Column(Float)
    wind_gust = Column(Float)
    pressure = Column(Float)
    precipitation = Column(Float)
    condition = Column(String)
    location = Column(String, nullable=False)
    
