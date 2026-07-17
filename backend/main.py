import os
import httpx
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db, init_db
from backend.models import Vehicle, Destination

app = FastAPI(title="Carbon Footprint API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OSRM_BASE = os.getenv("OSRM_URL", "http://router:5000")


@app.on_event("startup")
async def startup():
    await init_db()


# ── Vehicles ──────────────────────────────────────────────────────────

@app.get("/api/vehicles/")
async def get_vehicles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle).order_by(Vehicle.id))
    return [_vehicle_to_dict(v) for v in result.scalars().all()]


@app.get("/api/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    v = result.scalar_one_or_none()
    if v is None:
        raise HTTPException(404, "Vehicle not found")
    return _vehicle_to_dict(v)


@app.post("/api/vehicles/")
async def create_vehicle(data: dict, db: AsyncSession = Depends(get_db)):
    v = Vehicle(
        name=data.get("name", "New Vehicle"),
        home_address=data.get("homeAddress", ""),
        emission_factor=data.get("emissionFactor", 2.31),
        consumption=data.get("consumption", 8.5),
        study_settings=data.get("studySettings", {"studyName": "New Study", "studyDuration": 5, "workingHours": 8}),
    )
    db.add(v)
    await db.commit()
    await db.refresh(v)
    return _vehicle_to_dict(v)


@app.put("/api/vehicles/{vehicle_id}")
async def update_vehicle(vehicle_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    v = result.scalar_one_or_none()
    if v is None:
        raise HTTPException(404, "Vehicle not found")
    if "name" in data:
        v.name = data["name"]
    if "homeAddress" in data:
        v.home_address = data["homeAddress"]
    if "emissionFactor" in data:
        v.emission_factor = data["emissionFactor"]
    if "consumption" in data:
        v.consumption = data["consumption"]
    if "studySettings" in data:
        v.study_settings = data["studySettings"]
    await db.commit()
    await db.refresh(v)
    return _vehicle_to_dict(v)


@app.delete("/api/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    v = result.scalar_one_or_none()
    if v is None:
        raise HTTPException(404, "Vehicle not found")
    await db.delete(v)
    await db.commit()
    return {"ok": True}


# ── Destinations ─────────────────────────────────────────────────────

@app.get("/api/vehicles/{vehicle_id}/destinations/")
async def get_destinations(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Destination).where(Destination.vehicle_id == vehicle_id).order_by(Destination.id)
    )
    return [_dest_to_dict(d) for d in result.scalars().all()]


@app.post("/api/vehicles/{vehicle_id}/destinations/")
async def create_destination(vehicle_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    d = Destination(
        vehicle_id=vehicle_id,
        name=data.get("name", ""),
        address=data.get("address", ""),
        measurements=data.get("measurements", ""),
        duration=data.get("duration", 4),
        days=data.get("days", [1]),
        distance=data.get("distance", 0),
        round_trip_distance=data.get("roundTripDistance", 0),
        fuel_used=data.get("fuelUsed", 0),
        co2_emissions=data.get("co2Emissions", 0),
        lat=data.get("lat"),
        lng=data.get("lng"),
    )
    db.add(d)
    await db.commit()
    await db.refresh(d)
    return _dest_to_dict(d)


@app.put("/api/destinations/{dest_id}")
async def update_destination(dest_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Destination).where(Destination.id == dest_id))
    d = result.scalar_one_or_none()
    if d is None:
        raise HTTPException(404, "Destination not found")
    for field, col in [
        ("name", "name"), ("address", "address"), ("measurements", "measurements"),
        ("duration", "duration"), ("days", "days"), ("distance", "distance"),
        ("roundTripDistance", "round_trip_distance"), ("fuelUsed", "fuel_used"),
        ("co2Emissions", "co2_emissions"), ("lat", "lat"), ("lng", "lng"),
    ]:
        if field in data:
            setattr(d, col, data[field])
    await db.commit()
    await db.refresh(d)
    return _dest_to_dict(d)


@app.delete("/api/destinations/{dest_id}")
async def delete_destination(dest_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Destination).where(Destination.id == dest_id))
    d = result.scalar_one_or_none()
    if d is None:
        raise HTTPException(404, "Destination not found")
    await db.delete(d)
    await db.commit()
    return {"ok": True}


# ── Summary ──────────────────────────────────────────────────────────

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


# ── OSRM Routing ─────────────────────────────────────────────────────

@app.get("/api/route/{vehicle_id}")
async def get_optimized_route(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    """Calculate optimized route for a vehicle using OSRM."""
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    v = result.scalar_one_or_none()
    if v is None:
        raise HTTPException(404, "Vehicle not found")

    # Geocode home address if no coords
    home_coords = await _geocode(v.home_address)
    if not home_coords:
        raise HTTPException(400, f"Could not geocode home address: {v.home_address}")

    # Get all destinations with coords
    dests = []
    for d in v.destinations:
        lat = d.lat
        lng = d.lng
        if lat is None or lng is None:
            coords = await _geocode(d.address)
            if coords:
                lat, lng = coords
                d.lat = lat
                d.lng = lng
        if lat is not None and lng is not None:
            dests.append({"id": d.id, "lat": lat, "lng": lng, "days": d.days, "name": d.name})

    await db.commit()

    # Group by day and calculate routes
    day_routes = {}
    for d in dests:
        for day in d["days"]:
            if day not in day_routes:
                day_routes[day] = []
            day_routes[day].append(d)

    results = {}
    for day, sites in day_routes.items():
        if len(sites) == 1:
            # Simple round trip
            coords_str = f"{home_coords[1]},{home_coords[0]};{sites[0]['lng']},{sites[0]['lat']};{home_coords[1]},{home_coords[0]}"
            route = await _osrm_route(coords_str)
            results[day] = {
                "type": "round_trip",
                "distance": route["distance"] if route else 0,
                "duration": route["duration"] if route else 0,
                "geometry": route["geometry"] if route else None,
            }
        else:
            # Optimized route: home -> sites in order -> home
            coords = [f"{home_coords[1]},{home_coords[0]}"]
            for s in sites:
                coords.append(f"{s['lng']},{s['lat']}")
            coords.append(f"{home_coords[1]},{home_coords[0]}")
            route = await _osrm_route(";".join(coords))
            results[day] = {
                "type": "optimized",
                "distance": route["distance"] if route else 0,
                "duration": route["duration"] if route else 0,
                "geometry": route["geometry"] if route else None,
            }

    return results


async def _geocode(address: str) -> tuple | None:
    """Geocode an address using Nominatim (OSM)."""
    if not address:
        return None
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": address, "format": "json", "limit": 1},
                headers={"User-Agent": "CarbonFootprintApp/1.0"},
            )
            data = r.json()
            if data:
                return (float(data[0]["lat"]), float(data[0]["lon"]))
    except Exception:
        pass
    return None


async def _osrm_route(coords: str) -> dict | None:
    """Get route from OSRM."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(
                f"{OSRM_BASE}/route/v1/driving/{coords}",
                params={"overview": "full", "geometries": "geojson", "steps": "false"},
            )
            data = r.json()
            if data.get("code") == "Ok" and data.get("routes"):
                route = data["routes"][0]
                return {
                    "distance": route["distance"],
                    "duration": route["duration"],
                    "geometry": route["geometry"],
                }
    except Exception as e:
        print(f"OSRM route failed (OSRM may still be starting): {e}")
    return None


# ── Helpers ──────────────────────────────────────────────────────────

def _vehicle_to_dict(v: Vehicle) -> dict:
    return {
        "id": v.id,
        "name": v.name,
        "homeAddress": v.home_address,
        "emissionFactor": v.emission_factor,
        "consumption": v.consumption,
        "studySettings": v.study_settings or {"studyName": "New Study", "studyDuration": 5, "workingHours": 8},
        "destinations": [_dest_to_dict(d) for d in v.destinations],
    }


def _dest_to_dict(d: Destination) -> dict:
    return {
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
        "lat": d.lat,
        "lng": d.lng,
    }


if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
