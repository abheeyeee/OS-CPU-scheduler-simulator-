from typing import List
from collections import deque
from process import Process

def round_robin_schedule(processes: List[Process], time_quantum: int):
    processes.sort(key=lambda p: p.arrival_time)
    time = 0
    queue = deque()
    gantt = []
    remaining = {p.pid: p.burst_time for p in processes}
    arrived = []
    i = 0

    while i < len(processes) or queue:
        while i < len(processes) and processes[i].arrival_time <= time:
            queue.append(processes[i])
            i += 1

        if not queue:
            time += 1
            continue

        current = queue.popleft()

        if current.start_time is None:
            current.start_time = time

        run_time = min(time_quantum, remaining[current.pid])
        gantt.append((current.pid, time, time + run_time))
        time += run_time
        remaining[current.pid] -= run_time

        while i < len(processes) and processes[i].arrival_time <= time:
            queue.append(processes[i])
            i += 1

        if remaining[current.pid] > 0:
            queue.append(current)
        else:
            current.completion_time = time
            current.turnaround_time = time - current.arrival_time
            current.waiting_time = current.turnaround_time - current.burst_time

    return {"gantt": gantt, "processes": processes}