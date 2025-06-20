import json
from process import Process
from schedulers.fifo import fifo_schedule
from schedulers.round_robin import round_robin_schedule
from schedulers.mlfq import mlfq_schedule
from utils.visualizer import plot_gantt_chart
from schedulers.priority import priority_schedule
from schedulers.sjf import sjf_schedule
from schedulers.srtf import srtf_schedule 

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.start_time = None
        self.completion_time = None
        self.waiting_time = None
        self.turnaround_time = None

def load_processes(path):
    with open(path) as f:
        data = json.load(f)
        return [Process(**proc) for proc in data]

def main():
    processes = load_processes('input/sample_input.json')
    print("Choose scheduler:\n1. FIFO\n2. Round Robin\n3. MLFQ\n4. Priority Scheduling\n5. Shortest Job First (Non- Preemptive)\n6. SRTF (Preemptive SJF)")
    choice = input("Enter choice: ").strip()
    
    if choice == '1':
        result = fifo_schedule(processes)
    elif choice == '2':
        tq = int(input("Enter time quantum: "))
        result = round_robin_schedule(processes, time_quantum=tq)
    elif choice == '3':
        tq1 = int(input("TQ for Q0: "))
        tq2 = int(input("TQ for Q1: "))
        result = mlfq_schedule(processes, time_quantums=[tq1, tq2])
    elif choice == '4':
        result = priority_schedule(processes)
    elif choice == '5':
        result = sjf_schedule(processes)
    elif choice == '6':
        result = srtf_schedule(processes)
    else:
        print("Invalid choice")
        return

    plot_gantt_chart(result)
    print("\nProcess Summary:")
    for p in result["processes"]:
        print(f"P{p.pid} | WT: {p.waiting_time} | TAT: {p.turnaround_time} | CT: {p.completion_time}")

    avg_wt = sum(p.waiting_time for p in result["processes"]) / len(result["processes"])
    avg_tat = sum(p.turnaround_time for p in result["processes"]) / len(result["processes"])
    print(f"\nAverage Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")

if __name__ == "__main__":
    main()