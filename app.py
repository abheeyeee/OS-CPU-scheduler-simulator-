import streamlit as st
import json
from process import Process
from schedulers.fifo import fifo_schedule
from schedulers.round_robin import round_robin_schedule
from schedulers.mlfq import mlfq_schedule
from schedulers.priority import priority_schedule
from schedulers.sjf import sjf_schedule
from schedulers.srtf import srtf_schedule
from utils.visualizer import plot_gantt_chart, animate_gantt_chart
import matplotlib.pyplot as plt


if "simulated" not in st.session_state:
    st.session_state.simulated = False
    st.session_state.result = None
if "reset_input" not in st.session_state:
    st.session_state.reset_input = True

 
st.set_page_config(page_title="CPU Scheduler Simulator", layout="centered")
st.title("🔧 CPU Scheduling Simulator")
st.markdown("Built with ❤ using Streamlit")


col1, col2 = st.columns(2)
with col1:
    if st.button("🔄 Reset to Default JSON"):
        st.session_state.reset_input = True
with col2:
    if st.button("🧹 Clear Simulation"):
        st.session_state.simulated = False
        st.session_state.result = None

 
default_processes = [
    { "pid": 1, "arrival_time": 0, "burst_time": 8, "priority": 3 },
    { "pid": 2, "arrival_time": 1, "burst_time": 4, "priority": 1 },
    { "pid": 3, "arrival_time": 2, "burst_time": 9, "priority": 4 },
    { "pid": 4, "arrival_time": 3, "burst_time": 5, "priority": 2 },
    { "pid": 5, "arrival_time": 5, "burst_time": 2, "priority": 1 }
]

uploaded_file = st.file_uploader("📂 Upload JSON File (optional)", type=["json"])
if uploaded_file:
    try:
        raw_json = uploaded_file.read().decode("utf-8")
        raw_data = json.loads(raw_json)
        processes = [Process(**p) for p in raw_data]
    except Exception as e:
        st.error(f"❌ Invalid uploaded JSON: {e}")
        st.stop()
else:
    process_json = st.text_area("📥 Or Paste Process List (JSON)", json.dumps(default_processes, indent=2), height=200)
    try:
        raw_data = json.loads(process_json)
        processes = [Process(**p) for p in raw_data]
    except Exception as e:
        st.error(f"❌ Invalid pasted JSON: {e}")
        st.stop()

 
scheduler = st.selectbox("📋 Select Scheduler", [
    "FIFO", "Round Robin", "MLFQ", "Priority Scheduling", "SJF", "SRTF"
])


time_quantum = None
mlfq_tq1 = None
mlfq_tq2 = None
if scheduler == "Round Robin":
    time_quantum = st.number_input("Time Quantum", min_value=1, step=1)
elif scheduler == "MLFQ":
    mlfq_tq1 = st.number_input("Time Quantum Q0", min_value=1, step=1)
    mlfq_tq2 = st.number_input("Time Quantum Q1", min_value=1, step=1)

 
if st.button("▶ Run Simulation"):
    if scheduler == "FIFO":
        result = fifo_schedule(processes)
    elif scheduler == "Round Robin":
        result = round_robin_schedule(processes, time_quantum=int(time_quantum))
    elif scheduler == "MLFQ":
        result = mlfq_schedule(processes, time_quantums=[int(mlfq_tq1), int(mlfq_tq2)])
    elif scheduler == "Priority Scheduling":
        result = priority_schedule(processes)
    elif scheduler == "SJF":
        result = sjf_schedule(processes)
    elif scheduler == "SRTF":
        result = srtf_schedule(processes)

    st.session_state.result = result
    st.session_state.simulated = True

 
if st.session_state.simulated:
    result = st.session_state.result

    st.subheader("📊 Gantt Chart (Static)")
    fig = plot_gantt_chart(result)
    st.pyplot(fig)

    st.subheader("🎞️ Animated Gantt Chart")
    delay = st.slider("⏱️ Animation Delay (seconds)", 0.1, 1.0, 0.5, 0.1)
    animate_gantt_chart(result, delay=delay)

     
    st.subheader("📋 Process Summary")
    st.table([{
        "PID": f"P{p.pid}",
        "AT": p.arrival_time,
        "BT": p.burst_time,
        "CT": p.completion_time,
        "TAT": p.turnaround_time,
        "WT": p.waiting_time
    } for p in result["processes"]])

    avg_wt = sum(p.waiting_time for p in result["processes"]) / len(result["processes"])
    avg_tat = sum(p.turnaround_time for p in result["processes"]) / len(result["processes"])
    st.success(f"✅ Avg Waiting Time: {avg_wt:.2f} | Avg Turnaround Time: {avg_tat:.2f}")

     
    total_time = result["gantt"][-1][2]
    total_idle = sum(
        result["gantt"][i][1] - result["gantt"][i - 1][2]
        for i in range(1, len(result["gantt"]))
        if result["gantt"][i][1] > result["gantt"][i - 1][2]
    )
    cpu_util = ((total_time - total_idle) / total_time) * 100
    throughput = len(result["processes"]) / total_time

    st.info(f"💡 CPU Utilization: {cpu_util:.2f}%")
    st.info(f"📈 Throughput: {throughput:.2f} processes/unit time")

     
    algos_to_compare = st.multiselect(
        "📊 Compare Algorithms (Optional)", 
        ["FIFO", "Round Robin", "MLFQ", "Priority Scheduling", "SJF", "SRTF"]
    )

    if algos_to_compare:
        st.subheader("📈 Algorithm Comparison Summary")
        summary = []

        for algo in algos_to_compare:
            if algo == "FIFO":
                res = fifo_schedule(processes)
            elif algo == "Round Robin":
                res = round_robin_schedule(processes, time_quantum=2)
            elif algo == "MLFQ":
                res = mlfq_schedule(processes, time_quantums=[2, 4])
            elif algo == "Priority Scheduling":
                res = priority_schedule(processes)
            elif algo == "SJF":
                res = sjf_schedule(processes)
            elif algo == "SRTF":
                res = srtf_schedule(processes)

            avg_wt = sum(p.waiting_time for p in res["processes"]) / len(res["processes"])
            avg_tat = sum(p.turnaround_time for p in res["processes"]) / len(res["processes"])

            summary.append({
                "Algorithm": algo,
                "Avg WT": round(avg_wt, 2),
                "Avg TAT": round(avg_tat, 2)
            })

        st.table(summary)

     
    import pandas as pd

    df = pd.DataFrame([{
        "PID": p.pid,
        "Arrival Time": p.arrival_time,
        "Burst Time": p.burst_time,
        "Completion Time": p.completion_time,
        "Turnaround Time": p.turnaround_time,
        "Waiting Time": p.waiting_time
    } for p in result["processes"]])

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Process Summary as CSV", csv, "process_summary.csv", "text/csv")
