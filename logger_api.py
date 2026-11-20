import time
import random
import requests
from datetime import datetime

# API_URL = "https://machine-monitoring-api.onrender.com"
API_URL = "https://machine-monitoring-project.onrender.com"  # Alternative URL
# Simulated machine starting values
counter = 108
total = 20812

print("Logger started! Sending a reading every 30 seconds.")
print("Press CTRL + C to stop.")

while True:

    # Simulate machine activity
    produced = random.randint(0, 2)
    counter += produced
    total += produced

    reading = {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "counter": counter,
        "total": total
    }

    try:
        response = requests.post(
            f"{API_URL}/readings",
            json=reading,
            timeout=10
        )
        print("Sent:", reading, "| Status:", response.status_code)

    except Exception as error:
        print("Could not send, will try again:", error)

    time.sleep(30)