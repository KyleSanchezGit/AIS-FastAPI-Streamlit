import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()  # loads POSTGRES_* from .env

DB_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER')}:"
    f"{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('DB_HOST','localhost')}:"
    f"{os.getenv('DB_PORT','5432')}/"
    f"{os.getenv('POSTGRES_DB')}"
)
engine = create_engine(DB_URL, echo=False)

app = FastAPI(title="AIS FastAPI")

class Vessel(BaseModel):
    mmsi: int
    ts: str
    latitude: float
    longitude: float
    nav_status: str
    sog: float | None
    cog: float | None
    heading: int | None
    ship_name: str | None
    geom: dict | None

@app.get("/vessels/", response_model=list[Vessel])
def list_vessels(limit: int = 100):
    sql = text("""
      SELECT
        mmsi, ts, latitude, longitude,
        nav_status, sog, cog, heading,
        ship_name,
        ST_AsGeoJSON(geom)::json AS geom
      FROM public.ais_raw
      LIMIT :limit
    """)
    with engine.connect() as conn:
        rows = conn.execute(sql, {"limit": limit}).mappings().all()
    if not rows:
        raise HTTPException(404, "No data found")
    return [Vessel(**r) for r in rows]
