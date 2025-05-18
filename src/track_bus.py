import time
import datetime
import requests
from haversine import haversine

# Stop locations
ZOO = (59.42627177589917, 24.658942375776245)
TOOMPARK = (59.43682293950809, 24.73323876786831)
DISTANCE_THRESHOLD = 50  # meters

# Log file
LOG_FILE = "data/bus_arrivals.csv"

def read_gps():
    url = "https://transport.tallinn.ee/gps.txt"
    response = requests.get(url)
    lines = response.text.strip().split("\n")
    buses = []

    for line in lines:
        parts = line.split(",")
        if len(parts) < 10:
            continue
        if parts[0] != "2" or parts[1] != "8":
            continue
        lon = int(parts[2]) / 1_000_000
        lat = int(parts[3]) / 1_000_000
        vehicle_id = parts[6]
        buses.append((lat, lon, vehicle_id))
        print(buses)
    return buses

bus_at_stop = set()  # Tracks buses currently inside the stop zone

def track():
    while True:
        now = datetime.datetime.now()
        if now.hour == 9 and now.minute > 2:
            print("Done for the day.")
            break

        current_buses = set()
        for lat, lon, vehicle_id in read_gps():
            for stop_name, stop_coords in [("Zoo", ZOO), ("Toompark", TOOMPARK)]:
                distance = haversine(lat, lon, *stop_coords)
                key = (vehicle_id, stop_name)
                if distance < DISTANCE_THRESHOLD:
                    current_buses.add(key)

                    if key not in bus_at_stop:
                        # Bus just arrived
                        print(f"🟢 {vehicle_id} ARRIVED at {stop_name} at {now}")
                        with open(LOG_FILE, "a", encoding="utf-8") as f:
                            f.write(f"{now},{stop_name},{vehicle_id},arrived\n")
                elif key in bus_at_stop:
                    # Bus just left
                    print(f"🔴 {vehicle_id} DEPARTED from {stop_name} at {now}")
                    with open(LOG_FILE, "a", encoding="utf-8") as f:
                        f.write(f"{now},{stop_name},{vehicle_id},departed\n")

        bus_at_stop.clear()
        bus_at_stop.update(current_buses)
        time.sleep(5)

if __name__ == "__main__":
    track()