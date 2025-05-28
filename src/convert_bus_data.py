""" Clean and process raw bus arrival/departure logs """

import pandas as pd

def convert_bus_data(input_path="data/bus_arrivals.csv", output_path="data/clean_bus_times.csv"):
    """
    Reads raw arrival/departure logs and calculates the midpoint between each
    arrival and departure to estimate dwell center time. Saves cleaned output
    as a new CSV file.

    Args:
        input_path (str): Path to the raw bus arrivals file.
        output_path (str): Path to save the cleaned output.
    """
    df = pd.read_csv(input_path, header=None, names=["timestamp", "stop", "vehicle_id", "event"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    output = []
    pending = {}  # Temporarily holds arrival times until matched with departure

    for _, row in df.iterrows():
        key = (row["stop"], row["vehicle_id"])  # Unique identifier for each bus at a stop
        event = row["event"]
        ts = row["timestamp"]

        if event == "arrived":
            pending[key] = ts  # Store the arrival time for this bus at this stop
        elif event == "departed" and key in pending:  # Found a matching departure — calculate the midpoint
            arrival_time = pending.pop(key)
            mid_time = arrival_time + (ts - arrival_time) / 2

            # Add cleaned entry
            output.append({
                "stop": row["stop"],
                "vehicle_id": row["vehicle_id"],
                "mid_time": mid_time,
                "date": mid_time.date()
            })
    # Convert to DataFrame and save to CSV
    clean_df = pd.DataFrame(output)
    clean_df.to_csv(output_path, index=False)
    print(f"✅ Cleaned bus data saved to {output_path}")

# Run as a script
if __name__ == "__main__":
    convert_bus_data()