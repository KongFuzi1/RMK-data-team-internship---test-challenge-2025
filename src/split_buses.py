""" Split first 3 buses per day into separate CSV files """

import pandas as pd

def split_buses(file_path="data/clean_bus_times.csv"):
    """
    Splits the first three buses per day into separate CSVs (bus_1.csv, bus_2.csv, bus_3.csv),
    including both Zoo and Toompark stops, based on vehicle ID and date.
    """
    df = pd.read_csv(file_path, parse_dates=["mid_time"])

    # Separate Zoo and Toompark
    zoo_df = df[df["stop"] == "Zoo"].copy()
    toom_df = df[df["stop"] == "Toompark"].copy()

    # Sort Zoo entries to determine order
    zoo_df = zoo_df.sort_values(["date", "mid_time"])

    # Storage for each bus
    bus_groups = {"bus_1": [], "bus_2": [], "bus_3": []}

    for date, group in zoo_df.groupby("date"):
        group = group.sort_values("mid_time").head(3)  # first 3 buses of the day
        for i, label in enumerate(["bus_1", "bus_2", "bus_3"]):
            if i < len(group):
                row = group.iloc[i]
                vehicle_id = row["vehicle_id"]

                # Get matching Toompark record for same bus
                match = toom_df[(toom_df["vehicle_id"] == vehicle_id) & (toom_df["date"] == date)]
                if match.empty:
                    print(f"⚠️ No Toompark match for bus {vehicle_id} on {date}")

                combined = pd.concat([pd.DataFrame([row]), match])
                bus_groups[label].append(combined)

    # Save each group to a separate CSV
    for label, entries in bus_groups.items():
        result_df = pd.concat(entries)
        result_df.to_csv(f"data/{label}.csv", index=False)
        print(f"✅ Saved {label} data to data/{label}.csv")

# Run as a script
if __name__ == "__main__":
    split_buses()