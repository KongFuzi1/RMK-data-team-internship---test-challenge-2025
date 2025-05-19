""" Track Bus Arrivals/Departures for Bus Line 8 """

import time
import datetime
import requests
from haversine import haversine

""" Constants """
# GPS coordinates of bus stops
ZOO = (59.42627177589917, 24.658942375776245)
TOOMPARK = (59.436755463128314, 24.73321477694734)

DISTANCE_THRESHOLD = 50  # meters; how close a bus needs to be to count as "at the stop"
LOG_FILE = "data/bus_arrivals.csv"

""" State """
# Keeps track of buses currently within stop zone (to detect arrivals/departures)
bus_at_stop = set()


def read_gps():
    """
    Fetches real-time GPS data from Tallinn's public transport feed and filters it
    to include only vehicles on bus line number 8.

    Returns:
        List[Tuple[float, float, str]]: A list of tuples, each containing:
            - latitude (float)
            - longitude (float)
            - vehicle ID (str)
    """
    url = "https://transport.tallinn.ee/gps.txt"
    response = requests.get(url)
    lines = response.text.strip().split("\n")
    buses = []

    for line in lines:
        parts = line.split(",")
        if len(parts) < 10:
            continue
        if parts[0] != "2" or parts[1] != "8":
            continue  # Only include bus line 8
        lon = int(parts[2]) / 1_000_000
        lat = int(parts[3]) / 1_000_000
        vehicle_id = parts[6]
        buses.append((lat, lon, vehicle_id))
        print(buses)
    return buses


def track():
    """
    Monitors the arrival and departure of bus number 8 at the Zoo and Toompark stops.

    Every 5 seconds, this function:
    - Fetches real-time GPS data for bus line 8,
    - Calculates distance to each stop (Zoo, Toompark),
    - Detects if a bus enters or leaves the stop zone (within defined distance threshold),
    - Logs arrival/departure events to a CSV file with timestamps.

    Stops tracking automatically after 09:05 AM.
    """
    while True:
        now = datetime.datetime.now()
        if now.hour == 9 and now.minute > 10:  # Stop tracking after 09:05
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

        # Update state for the next cycle
        bus_at_stop.clear()
        bus_at_stop.update(current_buses)

        time.sleep(5)

if __name__ == "__main__":
    track()