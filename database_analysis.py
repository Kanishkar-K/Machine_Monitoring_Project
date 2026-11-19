import sqlite3

# Connect to our database
connection = sqlite3.connect("machine_readings.db")

cursor = connection.cursor()

# 1. Get the latest machine reading
cursor.execute("""
    SELECT timestamp, counter, total
    FROM readings
    ORDER BY id DESC
    LIMIT 1
""")

latest = cursor.fetchone()

print("\n========== LATEST MACHINE READING ==========")

if latest:
    print("Timestamp:", latest[0])
    print("Counter:", latest[1])
    print("Total:", latest[2])
else:
    print("No readings available.")


# 2. Count total saved readings
cursor.execute("""
    SELECT COUNT(*) FROM readings
""")

count = cursor.fetchone()[0]

print("\n========== DATABASE INFORMATION ==========")
print("Total readings stored:", count)


# 3. Get the first recorded reading
cursor.execute("""
    SELECT timestamp, counter, total
    FROM readings
    ORDER BY id ASC
    LIMIT 1
""")

first = cursor.fetchone()

if first:
    print("\n========== FIRST MACHINE READING ==========")
    print("Timestamp:", first[0])
    print("Counter:", first[1])
    print("Total:", first[2])


# 4. Calculate production difference
if latest and first:

    counter_production = latest[1] - first[1]
    total_production = latest[2] - first[2]

    print("\n========== PRODUCTION SUMMARY ==========")
    print("Counter difference:", counter_production)
    print("Total difference:", total_production)


connection.close()