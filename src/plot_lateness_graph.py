""" Plot lateness probability curve based on departure time """

import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import os

from compute_lateness_probabilities import compute_lateness_probabilities

def plot_lateness_graph():
    """
    Plots and saves the lateness probability curve from 07:50:00 to 09:10:00.
    The output graph (lateness_cdf.png) is saved to the 'output/' directory.
    """
    # Get probability values for each second in the time range
    data = compute_lateness_probabilities()

    # Convert time strings to datetime objects for accurate x-axis plotting
    times = [datetime.strptime(t, "%H:%M:%S") for t, _ in data]
    probs = [p for _, p in data]

    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Set up plot
    plt.style.use("dark_background")
    plt.figure(figsize=(12, 6))
    plt.plot(times, probs, color="orange", linewidth=4)

    # Format x-axis with HH:MM labels every 10 minutes
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
    plt.xticks(rotation=45)

    # Labels and styling
    plt.xlabel("Time Rita leaves home")
    plt.ylabel("Probability of Rita being late to meeting)")
    plt.title("Probability of Being Late vs Time Leaving Home")
    plt.ylim(0, 1.05)
    plt.grid(True, linestyle=":", alpha=0.3)

    # Save to output folder
    output_path = "output/lateness_cdf.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"✅ Graph saved to {output_path}")

    # Also show the graph
    plt.show()

# Run the function
if __name__ == "__main__":
    plot_lateness_graph()
