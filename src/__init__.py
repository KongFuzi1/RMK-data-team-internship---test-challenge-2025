"""
This package contains the source code for the RMK Rita's lateness analysis challenge.

Modules:
- Data collection from real-time GPS (track_bus.py)
- Data cleaning and processing (convert_bus_data.py, labeling.py)
- Probability calculation:
    • compute_lateness_probabilities.py – calculates lateness over a time range
    • get_lateness_probability.py – interactively estimates lateness for a specific time
- Visualization of lateness probability as a cumulative distribution function (plot_lateness_graph.py)
- Utility functions (haversine.py)
"""