from typing import List
from process import Process

def priority_schedule(processes: List[Process]):
    processes.sort(key=lambda p: (p.arrival_time, p.priority))  # Sort by arrival first

    time = 0
    gantt = []
    completed = []
    ready_queue = []

    while len(completed) < len(processes):
        # Add available processes to ready queue
        for p in processes:
            if p.arrival_time <= time and p not in completed and p not in ready_queue:
                ready_queue.append(p)

        if ready_queue:
            # Select process with highest priority (lower number = higher priority)
            ready_queue.sort(key=lambda p: p.priority)
            current = ready_queue.pop(0)

            if current.start_time is None:
                current.start_time = time

            current.completion_time = time + current.burst_time
            current.turnaround_time = current.completion_time - current.arrival_time
            current.waiting_time = current.turnaround_time - current.burst_time
            gantt.append((current.pid, time, current.completion_time))
            time = current.completion_time
            completed.append(current)
        else:
            time += 1  # idle

    return {
        "gantt": gantt,
        "processes": processes
    }