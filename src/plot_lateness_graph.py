import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
import os

from compute_lateness_probabilities import compute_lateness_probabilities

def plot_lateness_graph():
    data = compute_lateness_probabilities()

    # Convert time strings to datetime objects
    times = [datetime.strptime(t, "%H:%M:%S") for t, _ in data]
    probs = [p for _, p in data]

    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Plot setup
    plt.style.use("dark_background")
    plt.figure(figsize=(12, 6))
    plt.plot(times, probs, color="orange", linewidth=3)

    # X-axis formatting
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=10))
    plt.xticks(rotation=45)

    # Labels and styling
    plt.xlabel("Time leaving home")
    plt.ylabel("P(late to meeting)")
    plt.title("Jaotusfunktsioon – Probability of Being Late vs Time Leaving Home")
    plt.ylim(0, 1.05)
    plt.grid(True, linestyle=":", alpha=0.3)

    # Save to file
    output_path = "output/lateness_cdf.png"
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"✅ Graph saved to {output_path}")

    plt.show()

# Run the function
if __name__ == "__main__":
    plot_lateness_graph()
