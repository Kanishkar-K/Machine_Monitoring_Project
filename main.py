from fastapi import FastAPI, HTTPException
import sqlite3
from datetime import datetime, date
from pathlib import Path

# --------------------------------
# APPLICATION CONFIGURATION
# --------------------------------

app = FastAPI(
    title="Machine Monitoring API",
    description="Advanced API for monitoring machine production",
    version="2.0.0"
)

# Always use the database inside the project folder
DATABASE_FILE = Path(__file__).resolve().parent / "machine_readings.db"


# --------------------------------
# DATABASE CONNECTION
# --------------------------------

def get_database():

    connection = sqlite3.connect(DATABASE_FILE)

    connection.row_factory = sqlite3.Row

    return connection


# --------------------------------
# 1. HOMEPAGE API
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "Machine Monitoring API is running!",
        "status": "Success"
    }


# --------------------------------
# 2. GET LATEST READING
# --------------------------------

@app.get("/latest")
def get_latest_reading():

    connection = get_database()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT timestamp, counter, total
        FROM readings
        ORDER BY id DESC
        LIMIT 1
    """)

    reading = cursor.fetchone()

    connection.close()

    if reading is None:

        return {"message": "No readings available"}

    return dict(reading)


# --------------------------------
# 3. GET HISTORICAL READINGS
# --------------------------------

@app.get("/readings")
def get_all_readings():

    connection = get_database()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, timestamp, counter, total
        FROM readings
        ORDER BY id DESC
        LIMIT 100
    """)

    readings = cursor.fetchall()

    connection.close()

    return {
        "total_records_returned": len(readings),
        "readings": [dict(row) for row in readings]
    }


# --------------------------------
# 4. PRODUCTION SUMMARY
# --------------------------------

@app.get("/summary")
def production_summary():

    connection = get_database()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_records,
            MIN(counter) AS minimum_counter,
            MAX(counter) AS maximum_counter,
            MIN(total) AS minimum_total,
            MAX(total) AS maximum_total
        FROM readings
    """)

    result = cursor.fetchone()

    connection.close()

    if result["total_records"] == 0:

        return {"message": "No readings available"}

    return {
        "total_records": result["total_records"],

        "counter_production": (
            result["maximum_counter"] - result["minimum_counter"]
        ),

        "total_production": (
            result["maximum_total"] - result["minimum_total"]
        )
    }


# --------------------------------
# 5. DATE-WISE READINGS
# --------------------------------

@app.get("/readings/by-date")
def readings_by_date(reading_date: date):

    connection = get_database()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, timestamp, counter, total
        FROM readings
        WHERE date(timestamp) = ?
        ORDER BY id ASC
    """, (reading_date.isoformat(),))

    readings = cursor.fetchall()

    connection.close()

    return {
        "date": reading_date.isoformat(),
        "total_records": len(readings),
        "readings": [dict(row) for row in readings]
    }


# --------------------------------
# 6. TIME-RANGE READINGS
# --------------------------------

@app.get("/readings/range")
def readings_by_time(start: str, end: str):

    try:

        start_time = datetime.fromisoformat(start)
        end_time = datetime.fromisoformat(end)

        if start_time.tzinfo is None or end_time.tzinfo is None:
            raise ValueError("Timezone information is required")

        if start_time > end_time:
            raise ValueError("Start time must be before end time")

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    connection = get_database()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, timestamp, counter, total
        FROM readings
        WHERE datetime(timestamp) BETWEEN datetime(?) AND datetime(?)
        ORDER BY id ASC
    """, (start, end))

    readings = cursor.fetchall()

    connection.close()

    return {
        "start_time": start,
        "end_time": end,
        "total_records": len(readings),
        "readings": [dict(row) for row in readings]
    }


# --------------------------------
# 7. TOTAL RECORD COUNT
# --------------------------------

@app.get("/count")
def get_record_count():

    connection = get_database()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM readings
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return {
        "total_machine_readings": count
    }