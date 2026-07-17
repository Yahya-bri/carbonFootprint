import json
import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Carbon Footprint API", version="1.0.0")

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

DATA_PATH = Path(__file__).resolve().parent.parent / "data.json"


def _load_data() -> dict | None:
    if not DATA_PATH.exists():
        return None
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/vehicles/")
def get_vehicles():
    data = _load_data()
    if data is None:
        raise HTTPException(status_code=404, detail="data.json not found")
    return data.get("vehicles", [])


@app.get("/api/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id: int):
    data = _load_data()
    if data is None:
        raise HTTPException(status_code=404, detail="data.json not found")
    vehicles = data.get("vehicles", [])
    if vehicle_id < 0 or vehicle_id >= len(vehicles):
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicles[vehicle_id]


@app.get("/api/summary/")
def get_summary():
    data = _load_data()
    if data is None:
        raise HTTPException(status_code=404, detail="data.json not found")
    vehicles = data.get("vehicles", [])
    total_co2 = 0.0
    total_distance = 0.0
    total_fuel = 0.0
    total_destinations = 0
    for v in vehicles:
        for d in v.get("destinations", []):
            total_co2 += d.get("co2Emissions", 0)
            total_distance += d.get("roundTripDistance", 0)
            total_fuel += d.get("fuelUsed", 0)
            total_destinations += 1
    return {
        "totalVehicles": len(vehicles),
        "totalDestinations": total_destinations,
        "totalCo2Kg": round(total_co2, 2),
        "totalDistanceKm": round(total_distance, 2),
        "totalFuelLiters": round(total_fuel, 2),
        "exportDate": data.get("exportDate", ""),
    }


@app.get("/api/home-addresses/")
def get_home_addresses():
    data = _load_data()
    if data is None:
        raise HTTPException(status_code=404, detail="data.json not found")
    vehicles = data.get("vehicles", [])
    addresses = list({v["homeAddress"] for v in vehicles if v.get("homeAddress")})
    return addresses


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
