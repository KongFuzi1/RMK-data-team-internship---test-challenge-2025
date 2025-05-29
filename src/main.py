""" Run the full bus lateness analysis pipeline """

import os
from convert_bus_data import convert_bus_data
from split_buses import split_buses
from plot_lateness_graph import plot_lateness_graph

def delete_old_outputs():
    """
    Deletes previously generated output files to ensure clean pipeline results.

    Removes:
    - Cleaned data file ('clean_bus_times.csv')
    - Split bus files ('bus_1.csv', 'bus_2.csv', 'bus_3.csv')
    - Output graph ('lateness_cdf.png')
    """
    print("🧹 Cleaning up old output files...")
    files_to_delete = [
        "data/clean_bus_times.csv",
        "data/bus_1.csv",
        "data/bus_2.csv",
        "data/bus_3.csv",
        "output/lateness_cdf.png"
    ]

    for file in files_to_delete:
        try:
            os.remove(file)
            print(f"🗑️ Removed {file}")
        except FileNotFoundError:
            pass  # If file doesn't exist, no problem

def main():
    """
    Executes the full lateness analysis pipeline:
    - Cleans raw data
    - Splits into individual bus journeys
    - Plots lateness probability graph
    """
    delete_old_outputs()

    print("📥 Step 1: Cleaning raw bus arrival data...")
    convert_bus_data()

    print("🚌 Step 2: Splitting data into separate buses...")
    split_buses()

    print("📊 Step 3: Plotting lateness probability curve...")
    plot_lateness_graph()

    print("✅ All steps completed successfully.")

if __name__ == "__main__":
    main()