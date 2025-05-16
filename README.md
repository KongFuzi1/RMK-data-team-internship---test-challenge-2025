# RMK Data Team Internship – Test Challenge 2025

This project solves the RMK data team internship test challenge. The task is to model and visualize the probability that Rita, who travels by Tallinn city bus number 8, will be late to her 9:05 AM meeting, depending on when she leaves home.

## 🚀 Objective

Rita takes the bus from Zoo to Toompark every weekday. The simulation aims to estimate her probability of being late based on her departure time from home.

## 🧠 Approach

- Simulate a realistic bus schedule (e.g., every 10 minutes between 07:00 and 09:00).
- Add fixed walk times:
  - 5 minutes from home to Zoo stop
  - 4 minutes from Toompark to meeting room
- Randomize the bus ride duration (e.g., 12–20 minutes).
- For each departure time, run many simulations to calculate the probability of being late.

## 📁 Project Structure

rmk-bus-challenge-2025/
│
├── data/ # Simulated or real data
├── src/ # Python source code
│ ├── simulation.py # Bus schedule and commute simulation
│ ├── model.py # Probability calculations
│ └── plot.py # Plotting lateness probability
├── tests/ # Optional unit tests
├── .gitignore # Git ignore rules
├── README.md # Project documentation
├── requirements.txt # Python dependencies
└── LICENSE # MIT License