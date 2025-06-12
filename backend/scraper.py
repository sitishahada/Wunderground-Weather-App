# === backend/scraper.py ===
import time
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup as BS
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import WeatherData
import re

# Mapping of locations to Wunderground base URLs
STATION_URLS = {
    "malacca": "https://www.wunderground.com/history/daily/my/malacca/WMKM/date/",
    "kuantan": "https://www.wunderground.com/history/daily/my/kuantan/WMKD/date/",
    "bayan-lepas": "https://www.wunderground.com/history/daily/my/bayan-lepas/WMKP/date/",
    "segamat": "https://www.wunderground.com/history/daily/my/segamat/WMAZ/date/",
    "kerteh": "https://www.wunderground.com/history/daily/my/kerteh/WMKE/date/"
}

def render_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(10)

    page_source = driver.page_source
    driver.quit()
    return page_source

def clean_numeric(text):
    try:
        return float(re.sub(r"[^\d.\-]", "", text))
    except:
        return None

def run_scraper():
    today = datetime.today()
    date_str = today.strftime("%Y-%m-%d")

    for station, base_url in STATION_URLS.items():
        print(f"Scraping station: {station}")
        url = f"{base_url}{date_str}"
        html = render_page(url)
        soup = BS(html, "html.parser")

        table = soup.find("table")
        if not table:
            print(f"No table found for {station}.")
            continue

        rows = table.find_all("tr")
        records = []

        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) >= 10:
                time_str = cols[0].get_text(strip=True)
                try:
                    time_obj = datetime.strptime(time_str, "%I:%M %p").time()
                except:
                    continue

                record = WeatherData(
                    date=today.date(),
                    time=time_obj,
                    temperature=clean_numeric(cols[1].get_text()),
                    dew_point=clean_numeric(cols[2].get_text()),
                    humidity=clean_numeric(cols[3].get_text()),
                    wind=cols[4].get_text(strip=True),
                    wind_speed=clean_numeric(cols[5].get_text()),
                    wind_gust=clean_numeric(cols[6].get_text()),
                    pressure=clean_numeric(cols[7].get_text()),
                    precipitation=clean_numeric(cols[8].get_text()),
                    condition=cols[9].get_text(strip=True),
                    location=station
                )
                records.append(record)

        if records:
            db: Session = SessionLocal()
            db.bulk_save_objects(records)
            db.commit()
            db.close()
            print(f"Inserted {len(records)} weather records for {station} on {date_str}.")
        else:
            print(f"No weather records extracted for {station}.")
