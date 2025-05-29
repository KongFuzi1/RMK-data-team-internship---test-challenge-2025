""" Calculate lateness probabilities per second based on home departure time """

import pandas as pd
from datetime import datetime, time, timedelta

def compute_lateness_probabilities():
    """
    Computes the probability that Rita will be late to her 09:05 meeting based on 
    her home departure time.

    Assumes:
    - Rita takes exactly 5 minutes (300 seconds) to walk from home to the Zoo bus stop.
    - She will catch the first available bus (bus_1, bus_2, or bus_3) that arrives at or after she arrives.
    - She is late if the bus she catches arrives at Toompark later than 09:01:00.

    The function simulates departure times from 07:50:00 to 09:10:00 (inclusive), in 1-second increments.

    Returns:
        List[Tuple[str, float]]: A list of (time_str, P_late) pairs, where:
            - time_str (str): The time Rita leaves home in "HH:MM:SS" format.
            - P_late (float): The estimated probability that she arrives late.
    """
    # Load pre-labeled bus data
    b1 = pd.read_csv("data/bus_1.csv", parse_dates=["mid_time"])
    b2 = pd.read_csv("data/bus_2.csv", parse_dates=["mid_time"])
    b3 = pd.read_csv("data/bus_3.csv", parse_dates=["mid_time"])

    cutoff = time(9, 1)
    results = []

    def evaluate_bus(df, t_arrive):
        """
        Determines whether a bus is caught and whether it arrives on time.
        """
        zoo = df[df["stop"] == "Zoo"].copy()
        toom = df[df["stop"] == "Toompark"].copy()
        zoo["caught"] = zoo["mid_time"].apply(lambda t: t.time() >= t_arrive)
        toom["on_time"] = toom["mid_time"].apply(lambda t: t.time() <= cutoff)
        return zoo, toom

    def get_p_late(t_home):
        """
        Computes the probability of being late if Rita leaves home at t_home.
        """
        t_arrive = (t_home + timedelta(minutes=5)).time()

        # Evaluate all 3 buses for catch/on-time status
        zoo1, toom1 = evaluate_bus(b1, t_arrive)
        zoo2, toom2 = evaluate_bus(b2, t_arrive)
        zoo3, toom3 = evaluate_bus(b3, t_arrive)

        total_days = len(zoo1)

        # Probabilities for each bus
        P_catch_1 = zoo1["caught"].sum() / total_days
        P_late_1 = 1 - toom1["on_time"].sum() / total_days

        P_catch_2 = zoo2["caught"].sum() / total_days
        P_late_2 = 1 - toom2["on_time"].sum() / total_days

        P_catch_3 = zoo3["caught"].sum() / total_days
        P_late_3 = 1 - toom3["on_time"].sum() / total_days

        # If bus 1 is always caught and always on time → never late
        if P_catch_1 == 1.0 and P_late_1 == 0.0:
            return 0.0

        # Layered lateness probability
        return (1 - P_catch_1) * (
            (P_catch_2 * P_late_2) +
            ((1 - P_catch_2) * P_catch_3 * P_late_3) +
            ((1 - P_catch_2) * (1 - P_catch_3))
        )

    # Iterate second by second from 07:50:00 to 09:10:00
    start = datetime.strptime("07:50:00", "%H:%M:%S")
    end = datetime.strptime("09:10:00", "%H:%M:%S")
    current = start

    while current <= end:
        time_str = current.strftime("%H:%M:%S")
        p_late = get_p_late(current)
        results.append((time_str, round(p_late, 5)))  # rounded for clarity
        current += timedelta(seconds=1)

    return results
