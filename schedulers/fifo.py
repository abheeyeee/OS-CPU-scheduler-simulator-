from typing import List
from process import Process

def fifo_schedule(processes: List[Process]):
    processes.sort(key=lambda p: p.arrival_time)
    current_time = 0
    gantt = []

    for p in processes:
        if current_time < p.arrival_time:
            current_time = p.arrival_time
        p.start_time = current_time
        p.completion_time = current_time + p.burst_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        current_time = p.completion_time
        gantt.append((p.pid, p.start_time, p.completion_time))

    return {"gantt": gantt, "processes": processes}