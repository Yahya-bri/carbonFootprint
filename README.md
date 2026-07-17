# 🌍 Carbon Footprint Calculator — Fullstack (FastAPI + Vue 3 + PostgreSQL)

A fullstack carbon footprint calculator for construction site travel, built with **Vue 3** (Composition API) + **FastAPI** + **PostgreSQL**.

## Project Structure

```
carbonFootprint/
├── backend/              # FastAPI REST API
│   ├── main.py           # App, routes, CORS
│   ├── database.py       # Async SQLAlchemy + PostgreSQL
│   ├── models.py         # Vehicle & Destination ORM models
│   ├── seed.py           # Seed data from data.json
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Vue 3 + Vite SPA
│   ├── src/
│   │   ├── components/   # Dashboard, VehicleDetail (Composition API)
│   │   ├── assets/       # Tailwind CSS
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── data.json             # Carbon footprint data
├── app.html              # Original single-page app (legacy)
├── docker-compose.yml
└── README.md
```

## Quick Start

### Docker (Recommended)

```bash
docker compose up
```

This starts PostgreSQL, seeds the data, and launches both backend and frontend.

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/

### Manual (Development)

**1. Start PostgreSQL** (e.g., via Docker):
```bash
docker run -d --name carbon-pg \
  -e POSTGRES_USER=carbon \
  -e POSTGRES_PASSWORD=carbon \
  -e POSTGRES_DB=carbonfootprint \
  -p 5432:5432 postgres:16-alpine
```

**2. Backend:**
```bash
cd backend
pip install -r requirements.txt
python -m backend.seed    # Load data.json into PostgreSQL
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**3. Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vehicles/` | List all vehicles (with destinations) |
| GET | `/api/vehicles/:id/` | Vehicle detail |
| GET | `/api/summary/` | Aggregated totals |
| GET | `/api/home-addresses/` | Unique home addresses |

## Tech Stack

- **Frontend:** Vue 3 (Composition API), Vue Router, Tailwind CSS, Axios
- **Backend:** FastAPI, SQLAlchemy 2.0 (async), PostgreSQL
- **DevOps:** Docker Compose, Vite
