# 🔧 CPU Scheduling Simulator https://abheeyeee-os-cpu-scheduler-simulator.streamlit.app

An interactive CPU scheduling algorithm simulator built using **Streamlit**.  
It visualizes common CPU scheduling algorithms with animated Gantt charts and performance metrics.

---

## 🚀 Features

- 🎯 Supports 6 Algorithms:
  - FIFO
  - Round Robin
  - Priority Scheduling
  - Shortest Job First (SJF)
  - Shortest Remaining Time First (SRTF)
  - Multi-Level Feedback Queue (MLFQ)
- 📊 Static and Animated Gantt Charts
- 📈 Performance Metrics:
  - Average Waiting Time
  - Average Turnaround Time
  - CPU Utilization
  - Throughput
- 🧠 Algorithm Comparison Tool
- 📥 Upload or Paste Process JSON
- 📤 Download process summary as CSV

---

## 🖥️ Live Demo

👉 Try the live version here:  
https://abheeyeee-os-cpu-scheduler-simulator.streamlit.app

---

## 📂 Folder Structure
scheduler-simulator/

├── requirements.txt # Dependencies
├── process.py # Process class
├── input/sample_input.json # Sample input file (optional)
├── utils/
│ └── visualizer.py # Static and animated Gantt chart
└── schedulers/
├── fifo.py
├── round_robin.py
├── mlfq.py
├── priority.py
├── sjf.py
└── srtf.py


---

## 📥 Run Locally

```bash
# Clone the repository
git clone https://github.com/your-username/scheduler-simulator.git
cd scheduler-simulator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

🔧 Sample Input Format
[
  { "pid": 1, "arrival_time": 0, "burst_time": 8, "priority": 3 },
  { "pid": 2, "arrival_time": 1, "burst_time": 4, "priority": 1 },
  { "pid": 3, "arrival_time": 2, "burst_time": 9, "priority": 4 }
]

💡 Future Enhancements
Response time calculation

Context switch count

Custom themes and dark mode

Real-time control for animation playback
