🏭 Machine Monitoring System

A real-time Machine Monitoring System built using Python, FastAPI, Streamlit, and SQLite.

This project simulates industrial machine production data, collects machine readings, stores them in a database, and displays real-time machine performance through an interactive dashboard.

🚀 Project Overview

The Machine Monitoring System monitors machine production activity by continuously collecting simulated machine readings.

It consists of four main components:

1. Machine Simulator – Generates machine production readings.
2. Machine Logger – Collects readings and stores them in the database.
3. FastAPI Backend – Provides machine data through API endpoints.
4. Streamlit Dashboard – Displays machine status and production metrics.

✨ Key Features

* Real-time machine monitoring.
* Automated production data simulation.
* Machine reading collection and database storage.
* Live machine status monitoring.
* Production counter tracking.
* Total production monitoring.
* Interactive dashboard.
* API-based data access.

🛠️ Technologies Used

* Python
* FastAPI
* Streamlit
* SQLite
* Pandas
* REST API
* Git and GitHub

📂 Project Structure

Machine_Monitoring_Project/
│
├── .venv/
├── dashboard.py
├── main.py
├── machine_simulator.py
├── machine_logger.py
├── database.db
└── README.md

⚙️ Installation and Setup

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd Machine_Monitoring_Project

2. Create a virtual environment

python3 -m venv .venv

3. Activate the virtual environment

Mac/Linux:

source .venv/bin/activate

4. Install dependencies

pip install -r requirements.txt

▶️ How to Run the Project

Open four separate terminals in VS Code.

Activate the virtual environment in each terminal:

source .venv/bin/activate

Terminal 1 – Machine Simulator

python machine_simulator.py

Terminal 2 – Machine Logger

python machine_logger.py

Terminal 3 – FastAPI Backend

uvicorn main:app --reload

Terminal 4 – Streamlit Dashboard

streamlit run dashboard.py

📊 Dashboard

The Streamlit dashboard provides a visual interface for monitoring machine production activity and machine status.

🔌 API

The FastAPI backend provides endpoints to access machine monitoring data.

API documentation:

http://127.0.0.1:8000/docs

Latest machine readings:

http://127.0.0.1:8000/latest

🎯 Project Objective

The objective of this project is to demonstrate how industrial machine monitoring systems can collect, process, store, and visualize production data in real time.

👨‍💻 Author

Developed as a Machine Monitoring System project using Python and modern data visualization technologies.