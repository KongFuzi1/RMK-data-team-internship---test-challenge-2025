# 🚌 RMK Data Team Internship – Test Challenge 2025

This project addresses the RMK Data Team internship test challenge. The goal is to estimate the probability that **Rita**, who takes Tallinn city **bus number 8**, will be **late to her 9:05 AM meeting**, based on when she leaves home.

## 🎯 Objective

Rita travels every weekday from **Zoo** to **Toompark**. She walks 5 minutes to the Zoo bus stop. If she reaches **Toompark by 9:01**, she’ll be on time.  
The task is to simulate and visualize how her **lateness probability** depends on her departure time.

## 💡 Approach

This solution uses **real-time GPS logs** of bus number 8 rather than relying on official schedules, which were found to be inaccurate.

We:
- Collect and clean bus arrival/departure logs
- Identify the first 3 buses each day
- Estimate Rita’s chance of catching each one
- Model lateness as a function of her departure time
- Visualize the results with a cumulative probability curve

## 🧪 Model Logic

For any time Rita leaves home, we:
- Determine if she can catch an available bus
- Estimate if that bus will arrive **on or before 9:01**
- Compute:
    P_late = (1 - P_catch) × P_arrive_late

## 📊 Example Output

- **`output/lateness_cdf.png`** – Graph showing how late Rita is likely to be depending on her departure time from home.

## 📉 Real-World Observations

The scheduled 8:38 bus was expected at Toompark by 8:51. In reality, it arrived at **9:02**, meaning Rita would be late. Hence, the model discards the timetable and uses **observed data only**.

## ✅ How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python src/main.py
```
Note: Real-time GPS data collection is handled separately and is not part of the full pipeline here. The pipeline processes the already collected raw data logs.

## ⚡ Quick Lateness Probability Query

You can also directly check Rita’s lateness probability for any specific departure time using:

```bash
python src/get_lateness_probability.py
```