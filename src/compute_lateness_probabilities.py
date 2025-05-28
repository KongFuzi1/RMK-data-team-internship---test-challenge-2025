import pandas as pd
from datetime import datetime, time, timedelta

def compute_lateness_probabilities():
    """
    Calculates lateness probability for each second from 08:00:00 to 09:00:05.
    Returns a list of tuples: (time_str, probability).
    """
    # Load bus data
    b1 = pd.read_csv("data/bus_1.csv", parse_dates=["mid_time"])
    b2 = pd.read_csv("data/bus_2.csv", parse_dates=["mid_time"])
    b3 = pd.read_csv("data/bus_3.csv", parse_dates=["mid_time"])

    cutoff = time(9, 1)
    results = []

    def evaluate_bus(df, t_arrive):
        zoo = df[df["stop"] == "Zoo"].copy()
        toom = df[df["stop"] == "Toompark"].copy()
        zoo["caught"] = zoo["mid_time"].apply(lambda t: t.time() >= t_arrive)
        toom["on_time"] = toom["mid_time"].apply(lambda t: t.time() <= cutoff)
        return zoo, toom

    def get_p_late(t_home):
        t_arrive = (t_home + timedelta(minutes=5)).time()

        zoo1, toom1 = evaluate_bus(b1, t_arrive)
        zoo2, toom2 = evaluate_bus(b2, t_arrive)
        zoo3, toom3 = evaluate_bus(b3, t_arrive)

        total_days = len(zoo1)

        P_catch_1 = zoo1["caught"].sum() / total_days
        P_late_1 = 1 - toom1["on_time"].sum() / total_days

        P_catch_2 = zoo2["caught"].sum() / total_days
        P_late_2 = 1 - toom2["on_time"].sum() / total_days

        P_catch_3 = zoo3["caught"].sum() / total_days
        P_late_3 = 1 - toom3["on_time"].sum() / total_days

        if P_catch_1 == 1.0 and P_late_1 == 0.0:
            return 0.0

        return (1 - P_catch_1) * (
            (P_catch_2 * P_late_2) +
            ((1 - P_catch_2) * P_catch_3 * P_late_3) +
            ((1 - P_catch_2) * (1 - P_catch_3))
        )

    # Iterate second by second from 08:00:00 to 09:00:05
    start = datetime.strptime("08:00:00", "%H:%M:%S")
    end = datetime.strptime("09:00:05", "%H:%M:%S")
    current = start

    while current <= end:
        time_str = current.strftime("%H:%M:%S")
        p_late = get_p_late(current)
        results.append((time_str, round(p_late, 5)))  # rounded for clarity
        current += timedelta(seconds=1)

    return results
