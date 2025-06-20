from typing import List
from collections import deque
from process import Process

def mlfq_schedule(processes: List[Process], time_quantums=[4, 8], max_levels=2):
    processes.sort(key=lambda p: p.arrival_time)
    time = 0
    gantt = []
    queues = [deque() for _ in range(max_levels)]
    remaining = {p.pid: p.burst_time for p in processes}
    i = 0

    while i < len(processes) or any(queues):
        while i < len(processes) and processes[i].arrival_time <= time:
            queues[0].append(processes[i])
            i += 1

        executed = False
        for level in range(max_levels):
            if queues[level]:
                current = queues[level].popleft()

                if current.start_time is None:
                    current.start_time = time

                tq = time_quantums[level]
                run_time = min(tq, remaining[current.pid])
                gantt.append((current.pid, time, time + run_time))
                time += run_time
                remaining[current.pid] -= run_time

                while i < len(processes) and processes[i].arrival_time <= time:
                    queues[0].append(processes[i])
                    i += 1

                if remaining[current.pid] > 0:
                    queues[min(level + 1, max_levels - 1)].append(current)
                else:
                    current.completion_time = time
                    current.turnaround_time = time - current.arrival_time
                    current.waiting_time = current.turnaround_time - current.burst_time

                executed = True
                break

        if not executed:
            time += 1

    return {"gantt": gantt, "processes": processes}