# === backend/main.py ===
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database import SessionLocal, engine
from backend.models import Base, WeatherData
from backend.scraper import run_scraper
from sqlalchemy.orm import Session
from datetime import date

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/weather/latest")
def get_latest_weather():
    db: Session = SessionLocal()
    today = date.today()
    data = db.query(WeatherData).filter(WeatherData.date == today).all()
    db.close()
    if not data:
        raise HTTPException(status_code=404, detail="No data for today")
    return data

@app.get("/weather/{query_date}")
def get_weather_by_date(query_date: date):
    db: Session = SessionLocal()
    data = db.query(WeatherData).filter(WeatherData.date == query_date).all()
    db.close()
    if not data:
        raise HTTPException(status_code=404, detail="No data for given date")
    return data

@app.post("/scrape")
def trigger_scrape():
    run_scraper()
    return {"message": "Scraping complete"}
