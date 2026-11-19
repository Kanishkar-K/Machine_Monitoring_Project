import time
import random
from datetime import datetime

# Initial machine readings
counter = 108
total = 20812

print("===================================")
print("       MACHINE SIMULATOR")
print("===================================")

print("Machine started successfully!")
print("Generating readings every second...")
print("Press CTRL + C to stop.")
print("-----------------------------------")

try:

    while True:

        # Simulate production
        produced = random.randint(0, 2)

        counter += produced
        total += produced

        # Get current timestamp
        current_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        # Display readings
        print(
            f"Time: {current_time} | "
            f"Counter: {counter} | "
            f"Total: {total}"
        )

        # Wait for one second
        time.sleep(1)

except KeyboardInterrupt:

    print("\nMachine simulator stopped.")

    print("Final Counter:", counter)
    print("Final Total:", total)