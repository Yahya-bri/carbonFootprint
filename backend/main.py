import json
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db, init_db
from backend.models import Vehicle, Destination

app = FastAPI(title="Carbon Footprint API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/api/vehicles/")
async def get_vehicles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Vehicle).order_by(Vehicle.id)
    )
    vehicles = result.scalars().all()
    return [_vehicle_to_dict(v) for v in vehicles]


@app.get("/api/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Vehicle).where(Vehicle.id == vehicle_id)
    )
    vehicle = result.scalar_one_or_none()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return _vehicle_to_dict(vehicle)


@app.get("/api/summary/")
async def get_summary(db: AsyncSession = Depends(get_db)):
    v_count = await db.scalar(select(func.count(Vehicle.id)))
    d_count = await db.scalar(select(func.count(Destination.id)))
    co2 = await db.scalar(select(func.coalesce(func.sum(Destination.co2_emissions), 0)))
    dist = await db.scalar(select(func.coalesce(func.sum(Destination.round_trip_distance), 0)))
    fuel = await db.scalar(select(func.coalesce(func.sum(Destination.fuel_used), 0)))

    return {
        "totalVehicles": v_count or 0,
        "totalDestinations": d_count or 0,
        "totalCo2Kg": round(float(co2 or 0), 2),
        "totalDistanceKm": round(float(dist or 0), 2),
        "totalFuelLiters": round(float(fuel or 0), 2),
    }


@app.get("/api/home-addresses/")
async def get_home_addresses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Vehicle.home_address).distinct().order_by(Vehicle.home_address)
    )
    return [row[0] for row in result.all()]


def _vehicle_to_dict(v: Vehicle) -> dict:
    return {
        "id": v.id,
        "name": v.name,
        "homeAddress": v.home_address,
        "emissionFactor": v.emission_factor,
        "consumption": v.consumption,
        "studySettings": v.study_settings,
        "destinations": [
            {
                "id": d.id,
                "name": d.name,
                "address": d.address,
                "measurements": d.measurements,
                "duration": d.duration,
                "days": d.days,
                "distance": d.distance,
                "roundTripDistance": d.round_trip_distance,
                "fuelUsed": d.fuel_used,
                "co2Emissions": d.co2_emissions,
            }
            for d in v.destinations
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
