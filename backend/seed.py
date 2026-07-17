import json
import asyncio
from pathlib import Path

from backend.database import async_session, init_db
from backend.models import Vehicle, Destination


async def seed():
    data_path = Path(__file__).resolve().parent.parent / "data.json"
    if not data_path.exists():
        print("data.json not found, skipping seed")
        return

    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    await init_db()

    async with async_session() as session:
        for v in data.get("vehicles", []):
            vehicle = Vehicle(
                name=v["name"],
                home_address=v["homeAddress"],
                emission_factor=v["emissionFactor"],
                consumption=v["consumption"],
                study_settings=v.get("studySettings"),
            )
            session.add(vehicle)
            await session.flush()

            for d in v.get("destinations", []):
                dest = Destination(
                    vehicle_id=vehicle.id,
                    name=d.get("name", ""),
                    address=d.get("address", ""),
                    measurements=d.get("measurements", ""),
                    duration=d.get("duration", 0),
                    days=d.get("days", []),
                    distance=d.get("distance", 0),
                    round_trip_distance=d.get("roundTripDistance", 0),
                    fuel_used=d.get("fuelUsed", 0),
                    co2_emissions=d.get("co2Emissions", 0),
                )
                session.add(dest)

        await session.commit()
        print(f"Seeded {len(data.get('vehicles', []))} vehicles with destinations.")


if __name__ == "__main__":
    asyncio.run(seed())
