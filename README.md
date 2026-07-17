# 🌍 Carbon Footprint Calculator — Fullstack (Legacy-style + OSM + OSRM)

A fullstack carbon footprint calculator for construction site travel, matching the original legacy app's look and feel but with **OpenStreetMap** (Leaflet) and **OSRM** for local path routing.

## Features

- **Multi-vehicle management** — add/edit/delete vehicles with study settings
- **Site planning** — add field sites with addresses, measurements, duration, and days
- **OpenStreetMap** — interactive map with Leaflet, no API key needed
- **OSRM routing** — local path calculation using Open Source Routing Machine
- **CO₂ calculation** — automatic emissions based on distance, fuel consumption, and emission factor
- **Optimized routes** — multi-site days get optimized round trips (home → sites → home)
- **Charts** — CO₂ distribution pie chart per vehicle
- **Session export/import** — save and restore your data

## Quick Start

```bash
docker compose up
```

**Note:** The first run downloads OSRM data (~500MB) and builds the routing graph. This takes a few minutes.

- **App:** http://localhost
- **API:** http://localhost/api/

## Tech Stack

- **Frontend:** Vue 3 (Composition API), Leaflet/OSM, Chart.js, Tailwind CSS
- **Backend:** FastAPI, SQLAlchemy async, PostgreSQL
- **Routing:** OSRM (Open Source Routing Machine)
- **DevOps:** Docker Compose, Nginx
