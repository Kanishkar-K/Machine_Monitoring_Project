
import sqlite3

# Connect to the existing database
connection = sqlite3.connect("machine_readings.db")

cursor = connection.cursor()

# Retrieve all saved readings
cursor.execute("""
SELECT id, timestamp, counter, total
FROM readings
ORDER BY id DESC
""")

readings = cursor.fetchall()

print("\n===== MACHINE READING HISTORY =====\n")

if readings:
    for row in readings:
        print("ID:", row[0])
        print("Timestamp:", row[1])
        print("Counter:", row[2])
        print("Total:", row[3])
        print("--------------------------------")

else:
    print("No readings found.")

connection.close()
