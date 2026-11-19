import time
import random
import sqlite3
from datetime import datetime

# Starting simulated machine readings
counter = 108
total = 20812

# Connect to the database (creates it automatically)
connection = sqlite3.connect("machine_readings.db")
cursor = connection.cursor()

# Create a table to store readings
cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    counter INTEGER NOT NULL,
    total INTEGER NOT NULL
)
""")

connection.commit()

print("Machine monitoring started!")
print("Saving readings every 30 seconds.")
print("Press CTRL + C to stop.")

try:
    while True:

        # Simulate machine activity
        produced = random.randint(0, 2)
        counter += produced
        total += produced

        # Take a reading
        timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

        # Save reading to database
        cursor.execute(
            "INSERT INTO readings (timestamp, counter, total) VALUES (?, ?, ?)",
            (timestamp, counter, total)
        )

        connection.commit()

        print(
            f"Saved | {timestamp} | "
            f"Counter: {counter} | Total: {total}"
        )

        # Wait 30 seconds before the next reading
        time.sleep(30)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")

finally:
    connection.close()