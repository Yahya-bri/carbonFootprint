# 🌍 Carbon Footprint Calculator — Fullstack (FastAPI + Vue 3)

A fullstack carbon footprint calculator for construction site travel, built with **Vue 3** (frontend) + **FastAPI** (backend).

## Project Structure

```
carbonFootprint/
├── backend/              # FastAPI REST API
│   ├── main.py           # App, routes, CORS
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Vue 3 + Vite SPA
│   ├── src/
│   │   ├── components/   # Dashboard, VehicleDetail
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

### Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

API available at `http://localhost:8000/api/`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`

### Docker

```bash
docker compose up
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vehicles/` | List all vehicles |
| GET | `/api/vehicles/:id/` | Vehicle detail |
| GET | `/api/summary/` | Aggregated totals |
| GET | `/api/home-addresses/` | Unique home addresses |

## Tech Stack

- **Frontend:** Vue 3, Vue Router, Tailwind CSS, Axios
- **Backend:** FastAPI, Uvicorn, SQLite (ready for future models)
- **DevOps:** Docker Compose, Vite
