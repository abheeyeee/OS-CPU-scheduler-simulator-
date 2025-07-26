import streamlit as st
import json
import pandas as pd
from process import Process
from schedulers.fifo import fifo_schedule
from schedulers.round_robin import round_robin_schedule
from schedulers.mlfq import mlfq_schedule
from schedulers.priority import priority_schedule
from schedulers.sjf import sjf_schedule
from schedulers.srtf import srtf_schedule
from utils.visualizer import plot_gantt_chart, animate_gantt_chart

# ---------- Streamlit Config ----------
st.set_page_config(page_title="CPU Scheduler Simulator", layout="wide")
st.title("⚡ CPU Scheduling Algorithm Visualizer")
st.markdown("""
<script defer src="https://cloud.umami.is/script.js" data-website-id="693fea19-52bf-46e3-9203-e2bad61fed8d"></script>
""", unsafe_allow_html=True)


st.markdown("""
<style>
/* Center the title */
h1 {
    text-align: center !important;
    font-size: 2rem !important;  /* Adjust size for smaller screens */
    word-wrap: break-word;
}

/* For smaller devices */
@media (max-width: 768px) {
    h1 {
        font-size: 1.5rem !important;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- Custom CSS for Better UI ----------
st.markdown("""
<style>
.stButton > button {
    background-color: #00FFAA;
    color: black;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    border: none;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #00cc88;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- Session State ----------
if "simulated" not in st.session_state:
    st.session_state.simulated = False
    st.session_state.result = None


# ---------- Custom Process Input ----------
st.subheader("📝 Define Your Processes")
num_processes = st.number_input("Number of Processes", min_value=1, max_value=10, value=5)

processes = []

for i in range(num_processes):
    with st.expander(f"⚙ Configure Process P{i+1}", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            at = st.number_input(f"Arrival Time", min_value=0, max_value=20, value=i, step=1, key=f"at{i}")
        with col2:
            bt = st.number_input(f"Burst Time", min_value=1, max_value=20, value=5, step=1, key=f"bt{i}")
        with col3:
            pr = st.number_input(f"Priority", min_value=1, max_value=5, value=3, step=1, key=f"pr{i}")
        processes.append(Process(pid=i+1, arrival_time=at, burst_time=bt, priority=pr))

# ---------- Scheduler Selection ----------
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

# ---------- Run Simulation ----------
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

# ---------- Show Results ----------
if st.session_state.simulated:
    result = st.session_state.result

    st.subheader("📊 Gantt Charts")
    _, slider_col = st.columns([1, 1])
    with slider_col:
        delay = st.slider("⏱️ Animation Delay (seconds)", 0.1, 1.0, 0.5, 0.1)
    col1, col2 = st.columns([1, 1], gap="small")

    with col1:
        st.markdown("<h4 style='text-align: center;'>Static Gantt Chart</h4>", unsafe_allow_html=True)
        fig = plot_gantt_chart(result)
        fig.set_size_inches(6, 5.4) 
        st.pyplot(fig, use_container_width=True)

    with col2:
    # Keep slider above animated chart
        st.markdown("<h4 style='text-align: center;'>Animated Gantt Chart</h4>", unsafe_allow_html=True)
        fig.set_size_inches(6, 6) 
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

    # ---------- Algorithm Comparison ----------
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

    # ---------- CSV Export ----------
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
