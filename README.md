# Adventure-World
2025 S2 Fundamentals of Programming Project

🎢 Adventure World Simulation

A dynamic theme park simulation built with Python, OOP, and matplotlib

📌 Overview

Adventure World Simulation models a fully interactive theme park where rides, patrons, terrain, and weather all evolve over time.

The simulation visualizes:
- Ride operations & movement
- Patron roaming, queuing, and riding
- Terrain & time-of-day transitions
- Weather effects
- Real-time and final statistics

By adjusting parameters such as timestamps, number of patrons, ride colors, and map files, users can compare how different conditions affect the park’s behavior.

✨ Key Features

🎡 Rides

Implemented ride types:
- Ferris Wheel
- Drop Tower
- Hurricane
- Pirate Ship
Each ride includes:
- Unique movement logic
- Break time & ride duration
- Queue capacity
- Operating price
- Individual boundaries, entrances, and exits
- Patron movement while riding
Rides operate even when queues are empty to mimic real-world behavior.

🧍 Patrons
Patrons have:
- Name, color, marker, and target ride
- States: Roaming → Queuing → Riding → Roaming/Exit
- Random or targeted movement
- Boundary-aware navigation (main boundary, ride boundary, pond boundary)
- New patrons spawn every quarter of the total timestamp

🪪 Queue Management
- FIFO queue structure
- Queue length limits per ride
- Patrons automatically join queues when encountering them
- Patrons board when ride state becomes riding
- Multi-step queue movement logic

🌳 Terrain & Environment
Terrain is loaded from CSV files such as:
map_dawn.csv, map_morning.csv, map_sunset.csv, map_midnight.csv, map_mix.csv

Includes:
- Sky & ground
- Moving sun & moon
- Clouds
- Ponds
- Main park boundary & ride boundaries
Time-of-day transitions are visualized by sequentially updating terrain elements.

☔ Weather & UI Controls
Interactive buttons on the matplotlib interface:
- SpeedControl: speed up / slow down simulation
- WeatherControl: start/stop rain using scatter plot animation

📊 Real-Time & Final Statistics

Displayed using matplotlib subplots:
- Line plot: ride profit per timestamp
- Table plot: operations, ridership, revenue
- Scatter plot: patron movement distribution
  
Final statistics are automatically saved as:

Adventureworld Statistics YYYY-mm-dd_HH:MM:SS.png



🚀 How to Run

Requirements

Python 3.10+

Libraries: matplotlib, numpy, scipy, random, queue, names, csv, pandas, datetime

Interactive Mode : python3 adventureworld.py -i


Prompts for:
- Timestamps (200–500, default 300)
- Number of patrons (10–30, default 20)
- Ferris Wheel color
- Drop Tower color
Default map: map5.csv

Batch Mode : python3 adventureworld.py -f map_dawn.csv -p param1.csv


Parameter file includes:
- Simulation length
- Number of patrons
- Ride colors
Map file defines background elements (sky, ground, sun, moon, clouds).

📂 Project Structure

AdventureWorld/

  │
  
  ├── adventureworld.py
  
  ├── Rides.py

  ├── Patrons.py

  ├── Terrains.py

  ├── ButtonControl.py

  ├── Statistics.py

  ├── map_*.csv

  ├── param*.csv

  └── README.md



🧪 Showcase Scenarios
- Scenario 1
  Command: python3 adventureworld.py -f map_morning.csv -p scenario_param1.csv
  Setup: 10 patrons, 2 rides (Ferris Wheel, Drop Tower)
  Result:
  - Underutilized rides
  - Patron congestion near boundaries
  - Verified correct state transitions and boundary checks
<img width="1600" height="600" alt="Adventureworld Statistics scenario1" src="https://github.com/user-attachments/assets/e2ba4570-18a8-4367-b30b-53cf78060086" />


- Scenario 2
  Command: python3 adventureworld.py -f map_sunset.csv -p scenario_param2.csv
  Setup: 30 patrons, 3 rides
  Result:
  - Large queue at Hurricane near entrance
  - Crowding due to boundary avoidance
  - Patrons correctly exiting the park
<img width="1600" height="600" alt="Adventureworld Statistics scenario2" src="https://github.com/user-attachments/assets/855469bf-3650-4083-9c52-a51ffb0692c0" />


- Scenario 3
  Command: python3 adventureworld.py -f map_midnight.csv -p scenario_param3.csv
  Setup: 40 patrons, 4 rides
  Result:
  - Frequent queues at Hurricane & Pirate Ship
  - Pirate Ship highly profitable despite low frequency
  - Ferris Wheel near entrance had low ridership
<img width="1600" height="600" alt="Adventureworld Statistics scenario3" src="https://github.com/user-attachments/assets/d366aaec-84cd-48a1-8216-59e8c1af7849" />


🧩 Design Summary

Object-Oriented Structure
- Rides superclass → 4 ride subclasses
- Patrons class handles movement, boundaries, queue logic
- Terrains manages environment & time-of-day
- ButtonControl handles UI interactions
- Statistics contains LinePlot, TablePlot, ScatterPlot classes
The driver file adventureworld.py orchestrates all modules.
<img width="1409" height="1700" alt="2025 S2 FOP UML Class Diagram" src="https://github.com/user-attachments/assets/3a298966-c766-4e33-8f2d-a44afc865d43" />


🔮 Future Work
- Full animation for smoother ride & patron movement
- Tracking repeat visitation & ride popularity
- Time-of-day preference analysis
- Adding shops, buildings, and more realistic terrain

📚 References
(List preserved from your report)
- Matplotlib Documentation (Animation, Timers, Widgets, Gridspec, etc.)
- SciPy Gaussian Filter
- Names library
- PyPI & API references

