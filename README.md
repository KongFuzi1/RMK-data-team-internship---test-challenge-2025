# RMK Data Team Internship – Test Challenge 2025

This project solves the RMK data team internship test challenge. The task is to model and visualize the probability that Rita, who travels by Tallinn city bus number 8, will be late to her 9:05 AM meeting, depending on when she leaves home.

## 🚀 Objective

Rita takes the bus from Zoo to Toompark every weekday. The simulation aims to estimate her probability of being late based on her departure time from home.

## 🧠 Improved Approach

This solution models Rita’s probability of being late to her 9:05 AM meeting based on the real schedule of Tallinn city bus number 8.

## 🚍 Core Idea

Two key buses:

Bus #1 — Leaves Zoo at 8:38, arrives Toompark at 8:51 (safe option).

Bus #2 — Leaves Zoo at 8:48, arrives Toompark at exactly 9:01 (risky option).

Rita walks 5 minutes to the Zoo stop. Her chance of being on time depends on:

Whether she catches Bus #1, which may sometimes depart early.

If she misses it, whether Bus #2 is even a second late, in which case she will be late.

## 🎲 Probability Model

Let t_arrive be the time Rita arrives at the Zoo stop.

Calculate P(Bus #1 departs after t_arrive) → probability she catches Bus #1.

Let P(Bus #2 arrives after 9:01:00) → probability of being late if she misses Bus #1.

Total lateness probability: P_late = (1 - P_catch_Bus1) × P_Bus2_late

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