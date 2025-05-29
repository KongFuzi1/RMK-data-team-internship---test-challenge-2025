"""
RMK Data Challenge – Rita's Bus Lateness Analysis

This package analyzes the likelihood of Rita being late to a morning meeting based on real-time GPS data from Tallinn bus line 8.

Modules:
- track_bus.py – Collects and logs raw bus arrival/departure events using live GPS data
- convert_bus_data.py – Cleans the raw log into structured stop times with midpoint timestamps
- split_buses.py – Extracts the first three buses of each day for focused analysis
- compute_lateness_probabilities.py – Calculates lateness probability curve over the morning timeframe
- get_lateness_probability.py – Estimates Rita’s lateness for a specific departure time
- plot_lateness_graph.py – Visualizes the cumulative probability of being late
- haversine.py – Utility function to compute distance between coordinates
- main.py – Runs the full pipeline from raw data to final visualization
"""