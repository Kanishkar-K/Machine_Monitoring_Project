from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, date
import os

# --------------------------------
# APPLICATION CONFIGURATION
# --------------------------------

app = FastAPI(
    title="Machine Monitoring API",
    description="Advanced API for monitoring machine production",
    version="3.0.0"
)

DATABASE_URL = os.getenv("DATABASE_URL")


# --------------------------------
# DATABASE CONNECTION
# --------------------------------

def get_database():

    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is missing")

    return psycopg2.connect(
        DATABASE_URL,
        cursor_factory=RealDictCursor
    )


# --------------------------------
# CREATE DATABASE TABLE
# --------------------------------

@app.on_event("startup")
def create_table():

    connection = get_database()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ NOT NULL,
            counter BIGINT NOT NULL,
            total BIGINT NOT NULL
        )
    """)

    connection.commit()

    cursor.close()
    connection.close()


# --------------------------------
# MACHINE READING MODEL
# --------------------------------

class MachineReading(BaseModel):
    timestamp: datetime
    counter: int
    total: int


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
# 2. RECEIVE MACHINE READING
# --------------------------------

@app.post("/readings")
def receive_reading(reading: MachineReading):

    connection = get_database()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO readings (timestamp, counter, total)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (
            reading.timestamp,
            reading.counter,
            reading.total
        ))

        result = cursor.fetchone()

        connection.commit()

        return {
            "message": "Machine reading saved successfully",
            "id": result["id"]
        }

    except Exception as error:

        connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:

        cursor.close()
        connection.close()


# --------------------------------
# 3. GET LATEST READING
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

    cursor.close()
    connection.close()

    if reading is None:
        return {"message": "No readings available"}

    return dict(reading)


# --------------------------------
# 4. GET HISTORICAL READINGS
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

    cursor.close()
    connection.close()

    return {
        "total_records_returned": len(readings),
        "readings": [dict(row) for row in readings]
    }


# --------------------------------
# 5. PRODUCTION SUMMARY
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

    cursor.close()
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
# 6. DATE-WISE READINGS
# --------------------------------

@app.get("/readings/by-date")
def readings_by_date(reading_date: date):

    connection = get_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, timestamp, counter, total
        FROM readings
        WHERE timestamp::date = %s
        ORDER BY id ASC
    """, (reading_date,))

    readings = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "date": reading_date.isoformat(),
        "total_records": len(readings),
        "readings": [dict(row) for row in readings]
    }


# --------------------------------
# 7. TIME-RANGE READINGS
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
        WHERE timestamp BETWEEN %s AND %s
        ORDER BY id ASC
    """, (start_time, end_time))

    readings = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "start_time": start,
        "end_time": end,
        "total_records": len(readings),
        "readings": [dict(row) for row in readings]
    }


# --------------------------------
# 8. TOTAL RECORD COUNT
# --------------------------------

@app.get("/count")
def get_record_count():

    connection = get_database()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM readings
    """)

    count = cursor.fetchone()["total"]

    cursor.close()
    connection.close()

    return {
        "total_machine_readings": count
    }