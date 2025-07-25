from typing import List
from process import Process

def srtf_schedule(processes: List[Process]):
    n = len(processes)
    remaining = {p.pid: p.burst_time for p in processes}
    completed = []
    time = 0
    gantt = []
    last_pid = None

    while len(completed) < n:
        ready = [p for p in processes if p.arrival_time <= time and p not in completed and remaining[p.pid] > 0]
        
        if ready:
            current = min(ready, key=lambda p: remaining[p.pid])
            
            if current.start_time is None:
                current.start_time = time
            
            remaining[current.pid] -= 1

            if last_pid != current.pid:
                gantt.append((current.pid, time, time + 1))
            else:
                gantt[-1] = (current.pid, gantt[-1][1], time + 1)

            if remaining[current.pid] == 0:
                current.completion_time = time + 1
                current.turnaround_time = current.completion_time - current.arrival_time
                current.waiting_time = current.turnaround_time - current.burst_time
                completed.append(current)

            last_pid = current.pid
        else:
            last_pid = None  
            gantt.append(("Idle", time, time + 1))

        time += 1

    return {
        "gantt": gantt,
        "processes": processes
    }