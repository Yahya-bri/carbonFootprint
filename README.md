# 🌍 Carbon Footprint Calculator — Fullstack

A fullstack carbon footprint calculator for construction site travel, built with **Vue 3** (frontend) + **Django REST Framework** (backend).

## Project Structure

```
carbonFootprint/
├── backend/              # Django REST API
│   ├── api/              # API app (views, urls)
│   ├── config/           # Django settings, URLs, WSGI
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
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
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
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

## Tech Stack

- **Frontend:** Vue 3, Vue Router, Tailwind CSS, Axios, Chart.js
- **Backend:** Django 5, Django REST Framework, SQLite
- **DevOps:** Docker Compose, Vite
