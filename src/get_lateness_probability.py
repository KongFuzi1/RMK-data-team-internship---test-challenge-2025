""" Interactive tool to estimate Rita's lateness probability based on her home departure time """

import pandas as pd
from datetime import datetime, time, timedelta

def get_lateness_probability_from_home_departure():
    """
    Asks the user for the time Rita leaves home and calculates the probability of her being late.
    The logic considers real GPS data, walking time to the bus stop, and multiple bus options.

    Bus structure:
        - bus_1.csv: earliest bus
        - bus_2.csv: second bus
        - bus_3.csv: third bus

    Rita must arrive at Toompark stop by 09:01:00 to avoid being late.
    """
    # Load preprocessed mid-time data for the 3 buses
    b1 = pd.read_csv("data/bus_1.csv", parse_dates=["mid_time"])
    b2 = pd.read_csv("data/bus_2.csv", parse_dates=["mid_time"])
    b3 = pd.read_csv("data/bus_3.csv", parse_dates=["mid_time"])

    # Prompt user until a valid time is entered
    while True:
        user_input = input("🏠 Enter the time Rita leaves home (HH:MM:SS): ")
        try:
            t_home = datetime.strptime(user_input.strip(), "%H:%M:%S")
            break  # valid, exit loop
        except ValueError:
            print("❌ Invalid format. Please enter time as HH:MM:SS (e.g. 08:28:00)")

    # Rita arrives at Zoo 5 minutes later
    t_arrive = (t_home + timedelta(seconds=300)).time()
    print(f"🚶 Arrival at Zoo stop after 5-minute walk: {t_arrive}")

    cutoff = time(9, 1)  # Latest allowed arrival time at Toompark to avoid being late

    def evaluate_bus(df):
        """
        Determines whether each bus on each day was:
        - Caught (based on Zoo stop timing)
        - On time (based on Toompark stop timing)
        """
        zoo = df[df["stop"] == "Zoo"].copy()
        toom = df[df["stop"] == "Toompark"].copy()
        zoo["caught"] = zoo["mid_time"].apply(lambda t: t.time() >= t_arrive)
        toom["on_time"] = toom["mid_time"].apply(lambda t: t.time() <= cutoff)
        return zoo, toom

    # Evaluate all 3 buses
    zoo1, toom1 = evaluate_bus(b1)
    zoo2, toom2 = evaluate_bus(b2)
    zoo3, toom3 = evaluate_bus(b3)

    total_days = len(zoo1)

    # Compute per-bus probabilities from data
    P_catch_1 = zoo1["caught"].sum() / total_days
    P_late_1 = 1 - toom1["on_time"].sum() / total_days

    P_catch_2 = zoo2["caught"].sum() / total_days
    P_late_2 = 1 - toom2["on_time"].sum() / total_days

    P_catch_3 = zoo3["caught"].sum() / total_days
    P_late_3 = 1 - toom3["on_time"].sum() / total_days

    # Early exit: if Rita always catches the first bus and it's always on time
    if P_catch_1 == 1.0 and P_late_1 == 0.0:
        print(f"✅ Rita is guaranteed to be on time if she leaves at {user_input}!")
        return 0.0

    # Tree-based probability calculation
    P_late = (1 - P_catch_1) * (
        (P_catch_2 * P_late_2) +
        ((1 - P_catch_2) * P_catch_3 * P_late_3) +
        ((1 - P_catch_2) * (1 - P_catch_3))
    )

    print(f"🧮 Leaving home at {user_input} → Estimated probability of being late: {P_late:.2%}")
    return P_late

if __name__ == "__main__":
    get_lateness_probability_from_home_departure()