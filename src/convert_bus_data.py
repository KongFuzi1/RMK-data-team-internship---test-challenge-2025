import pandas as pd
from datetime import datetime

# Read raw data
df = pd.read_csv("data/bus_arrivals.csv", header=None, names=["timestamp", "stop", "vehicle_id", "event"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

output = []

# Temporary store to hold pending arrivals
pending = {}

# Iterate row by row, preserving order
for _, row in df.iterrows():
    key = (row["stop"], row["vehicle_id"])
    event = row["event"]
    ts = row["timestamp"]

    if event == "arrived":
        pending[key] = ts  # Save arrival time
    elif event == "departed" and key in pending:
        arrival_time = pending.pop(key)
        mid_time = arrival_time + (ts - arrival_time) / 2
        output.append({
            "stop": row["stop"],
            "vehicle_id": row["vehicle_id"],
            "mid_time": mid_time,
            "date": mid_time.date()
        })

# Save cleaned output
clean_df = pd.DataFrame(output)
clean_df.to_csv("data/clean_bus_times.csv", index=False)

print("✅ Cleaned bus data saved in original order to data/clean_bus_times.csv")