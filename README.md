# RMK Data Team Internship – Test Challenge 2025

This project solves the RMK data team internship test challenge. The task is to model and visualize the probability that Rita, who travels by Tallinn city bus number 8, will be late to her 9:05 AM meeting, depending on when she leaves home.

## 🚀 Objective

Rita takes the bus from Zoo to Toompark every weekday. The simulation aims to estimate her probability of being late based on her departure time from home.

## 🧠 Improved Approach

This solution models Rita’s probability of being late to her 9:05 AM meeting based on the real schedule of Tallinn city bus number 8.

## 🚍 Core Idea

The initial assumption was based on the official bus timetable, which suggested:

Bus #1 — Leaves Zoo at 8:38, arrives Toompark at 8:51 (safe option)

Bus #2 — Leaves Zoo at 8:48, arrives Toompark at 9:01 (risky option)

However, real-time tracking revealed that these scheduled times are not accurate. For example, the bus scheduled to arrive at Toompark at 8:51 actually arrived at 9:01, showing a 10-minute deviation.

As a result, the model no longer relies on the published timetable, but instead uses real observed arrival and departure times, which are logged automatically from GPS data.

Rita walks 5 minutes to the Zoo stop. Whether she arrives at her 9:05 meeting depends on:

If she catches a bus that arrives at Toompark on or before 9:01

And whether that bus is actually on time, according to tracking data

## 🎲 Probability Model

Let t_arrive be the time Rita arrives at the Zoo stop (based on her home departure time).

We calculate:

P_catch_Bus1: The probability that a bus from Zoo departs at or after t_arrive

P_Bus2_arrives_late: The probability that the next available bus arrives at Toompark after 9:01:00

Then we compute:
P_late = (1 - P_catch_Bus1) × P_Bus2_arrives_late

## ⚠️ Problems Encountered

During data collection, I discovered a discrepancy in the official timetable for bus number 8.

According to the schedule:

A bus that departs from Zoo at 8:38 is expected to arrive at Toompark at 8:51.

However, based on real-time tracking:

That same bus actually arrived at Toompark at 9:02, 11 minutes later than scheduled.

This indicates that the published schedule may be inaccurate or outdated, at least during morning rush hours. Because of this, the model avoids relying on scheduled arrival times and instead uses observed data from GPS tracking.

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