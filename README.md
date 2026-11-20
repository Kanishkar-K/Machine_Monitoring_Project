# 🏭 Machine Monitoring System

A cloud-based system that collects machine readings every 30 seconds, stores them in a database, and shows them on a password-protected dashboard that works on mobile.

Currently tested with a **simulated machine**. The next phase connects the real PLC machine.

## How it works

Machine/PLC (simulated for now) → Logger → API (Render) → Database (Neon PostgreSQL) → Dashboard (Streamlit)

## Components

| File | Purpose |
|---|---|
| `machine_simulator.py` | Generates fake machine readings for testing |
| `logger_api.py` | Sends a reading to the API every 30 seconds |
| `main.py` | FastAPI backend, secured with an API key |
| `dashboard.py` | Streamlit dashboard with login, charts, CSV export, anomaly and downtime analysis |

## Technologies

Python, FastAPI, PostgreSQL (Neon), Streamlit, Render, GitHub

## Features

- Live machine status (running / stopped)
- Latest reading, history, date filter, CSV download
- Production charts, efficiency, anomaly and downtime analysis
- Password-protected dashboard, API-key-protected backend
- Works on mobile (add to home screen)

## Run the logger

    pip install requests
    export API_KEY="your-api-key"
    python logger_api.py

## Hosting (all free tiers)

- API: Render
- Database: Neon
- Dashboard: Streamlit Community Cloud

## Next phase

- Replace the simulator with real PLC readings
- Support multiple machines
- Native Android / iOS app

## Author

Developed as a student project for machine production monitoring.