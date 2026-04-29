"""
All OS algorithms — CPU Scheduling, Memory Management, Deadlock, Disk Scheduling.
Pure Python implementations for the UI.
"""
from collections import deque
import random

# ═══════════════════════════════════════════════════════════════════════════════
# CPU SCHEDULING
# ═══════════════════════════════════════════════════════════════════════════════

def fcfs(processes):
    """FCFS: First Come First Served. processes = [(pid, arrival, burst, priority)]"""
    procs = sorted(processes, key=lambda x: (x[1], x[0]))
    time, result, gantt = 0, [], []
    for pid, arrival, burst, _ in procs:
        if time < arrival:
            time = arrival
        wt = time - arrival
        gantt.append((pid, time, time + burst))
        time += burst
        result.append((pid, arrival, burst, wt, wt + burst))
    return result, gantt


def sjf(processes):
    """SJF: Shortest Job First (Non-Preemptive)."""
    procs = [list(p) for p in processes]
    time, result, gantt = 0, [], []
    remaining = procs[:]
    while remaining:
        available = [p for p in remaining if p[1] <= time]
        if not available:
            time = min(p[1] for p in remaining)
            available = [p for p in remaining if p[1] <= time]
        chosen = min(available, key=lambda x: (x[2], x[1]))
        remaining.remove(chosen)
        pid, arrival, burst = chosen[0], chosen[1], chosen[2]
        if time < arrival:
            time = arrival
        wt = time - arrival
        gantt.append((pid, time, time + burst))
        time += burst
        result.append((pid, arrival, burst, wt, wt + burst))
    return result, gantt


def srtf(processes):
    """SRTF: Shortest Remaining Time First (Preemptive SJF)."""
    n = len(processes)
    pids = [p[0] for p in processes]
    arrivals = [p[1] for p in processes]
    bursts = [p[2] for p in processes]
    remaining = bursts[:]
    completed = [False] * n
    time, done = 0, 0
    finish_time = [0] * n
    gantt = []
    prev_pid = -1

    while done < n:
        idx = -1
        min_rem = float('inf')
        for i in range(n):
            if arrivals[i] <= time and not completed[i] and remaining[i] < min_rem:
                min_rem = remaining[i]
                idx = i
        if idx == -1:
            time += 1
            continue

        if prev_pid != pids[idx]:
            if gantt and gantt[-1][0] == pids[idx]:
                pass
            gantt.append((pids[idx], time, time + 1))
        else:
            gantt[-1] = (gantt[-1][0], gantt[-1][1], time + 1)

        remaining[idx] -= 1
        time += 1
        prev_pid = pids[idx]

        if remaining[idx] == 0:
            completed[idx] = True
            done += 1
            finish_time[idx] = time

    result = []
    for i in range(n):
        wt = finish_time[i] - arrivals[i] - bursts[i]
        tat = finish_time[i] - arrivals[i]
        result.append((pids[i], arrivals[i], bursts[i], wt, tat))
    return result, gantt


def round_robin(processes, quantum):
    """Round Robin scheduling."""
    procs = sorted(processes, key=lambda x: x[1])
    n = len(procs)
    remaining = [p[2] for p in procs]
    arrival = [p[1] for p in procs]
    burst = [p[2] for p in procs]
    pids = [p[0] for p in procs]
    finish = [0] * n
    queue = deque()
    time, i = 0, 0
    visited = [False] * n
    gantt = []

    while i < n and arrival[i] <= time:
        queue.append(i)
        visited[i] = True
        i += 1

    while queue:
        idx = queue.popleft()
        run = min(quantum, remaining[idx])
        gantt.append((pids[idx], time, time + run))
        time += run
        remaining[idx] -= run

        while i < n and arrival[i] <= time:
            if not visited[i]:
                queue.append(i)
                visited[i] = True
            i += 1

        if remaining[idx] > 0:
            queue.append(idx)
        else:
            finish[idx] = time

    result = []
    for j in range(n):
        wt = finish[j] - arrival[j] - burst[j]
        result.append((pids[j], arrival[j], burst[j], wt, finish[j] - arrival[j]))
    return result, gantt


def priority_scheduling(processes):
    """Priority Scheduling (Non-Preemptive). Lower value = higher priority."""
    procs = [list(p) for p in processes]
    time, result, gantt = 0, [], []
    remaining = procs[:]
    while remaining:
        available = [p for p in remaining if p[1] <= time]
        if not available:
            time = min(p[1] for p in remaining)
            available = [p for p in remaining if p[1] <= time]
        chosen = min(available, key=lambda x: (x[3], x[1]))
        remaining.remove(chosen)
        pid, arrival, burst, pri = chosen
        if time < arrival:
            time = arrival
        wt = time - arrival
        gantt.append((pid, time, time + burst))
        time += burst
        result.append((pid, arrival, burst, wt, wt + burst))
    return result, gantt


def multilevel_queue(processes, quantum=2):
    """
    Multilevel Queue: 3 queues.
    Priority 1 = System (FCFS), Priority 2 = Interactive (RR), Priority 3 = Batch (FCFS).
    Queue levels based on process priority field: 1=high, 2=mid, 3=low.
    """
    q1 = sorted([p for p in processes if p[3] == 1], key=lambda x: x[1])
    q2 = sorted([p for p in processes if p[3] == 2], key=lambda x: x[1])
    q3 = sorted([p for p in processes if p[3] == 3], key=lambda x: x[1])

    time, result, gantt = 0, [], []

    # Queue 1: FCFS (highest priority)
    for pid, arrival, burst, pri in q1:
        if time < arrival:
            time = arrival
        wt = time - arrival
        gantt.append((pid, time, time + burst))
        time += burst
        result.append((pid, arrival, burst, wt, wt + burst))

    # Queue 2: Round Robin
    if q2:
        remaining = {p[0]: p[2] for p in q2}
        arr_map = {p[0]: p[1] for p in q2}
        burst_map = {p[0]: p[2] for p in q2}
        queue = deque([p[0] for p in q2 if p[1] <= time])
        added = set(queue)
        while queue or any(r > 0 for r in remaining.values()):
            for p in q2:
                if p[0] not in added and p[1] <= time:
                    queue.append(p[0])
                    added.add(p[0])
            if not queue:
                time += 1
                continue
            pid = queue.popleft()
            run = min(quantum, remaining[pid])
            gantt.append((pid, time, time + run))
            time += run
            remaining[pid] -= run
            for p in q2:
                if p[0] not in added and p[1] <= time:
                    queue.append(p[0])
                    added.add(p[0])
            if remaining[pid] > 0:
                queue.append(pid)
            else:
                wt = time - arr_map[pid] - burst_map[pid]
                tat = time - arr_map[pid]
                result.append((pid, arr_map[pid], burst_map[pid], wt, tat))

    # Queue 3: FCFS (lowest priority)
    for pid, arrival, burst, pri in q3:
        if time < arrival:
            time = arrival
        wt = time - arrival
        gantt.append((pid, time, time + burst))
        time += burst
        result.append((pid, arrival, burst, wt, wt + burst))

    return result, gantt


def mlfq(processes, q1_quantum=1, q2_quantum=2):
    """
    Multilevel Feedback Queue (MLFQ).
    Queue 1: RR with q1_quantum (highest priority)
    Queue 2: RR with q2_quantum
    Queue 3: FCFS (lowest priority)
    New processes enter Queue 1. If not finished, demoted to Queue 2, then Queue 3.
    """
    procs = sorted(processes, key=lambda x: x[1])
    n = len(procs)
    remaining = {p[0]: p[2] for p in procs}
    arrival = {p[0]: p[1] for p in procs}
    burst = {p[0]: p[2] for p in procs}
    finish = {}
    queue_level = {p[0]: 1 for p in procs}

    q1, q2, q3 = deque(), deque(), deque()
    time, idx = 0, 0
    gantt = []
    added = set()

    def enqueue_new():
        nonlocal idx
        while idx < n and procs[idx][1] <= time:
            pid = procs[idx][0]
            if pid not in added:
                q1.append(pid)
                added.add(pid)
            idx += 1

    enqueue_new()

    while q1 or q2 or q3 or idx < n:
        enqueue_new()
        if q1:
            pid = q1.popleft()
            run = min(q1_quantum, remaining[pid])
            gantt.append((pid, time, time + run))
            time += run
            remaining[pid] -= run
            enqueue_new()
            if remaining[pid] > 0:
                queue_level[pid] = 2
                q2.append(pid)
            else:
                finish[pid] = time
        elif q2:
            pid = q2.popleft()
            run = min(q2_quantum, remaining[pid])
            gantt.append((pid, time, time + run))
            time += run
            remaining[pid] -= run
            enqueue_new()
            if remaining[pid] > 0:
                queue_level[pid] = 3
                q3.append(pid)
            else:
                finish[pid] = time
        elif q3:
            pid = q3.popleft()
            run = remaining[pid]
            gantt.append((pid, time, time + run))
            time += run
            remaining[pid] = 0
            finish[pid] = time
            enqueue_new()
        else:
            time += 1
            enqueue_new()

    result = []
    for p in procs:
        pid = p[0]
        wt = finish.get(pid, 0) - arrival[pid] - burst[pid]
        tat = finish.get(pid, 0) - arrival[pid]
        result.append((pid, arrival[pid], burst[pid], max(0, wt), max(0, tat)))
    return result, gantt


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def first_fit(blocks, processes):
    """First Fit memory allocation. Returns [(proc_size, block_idx or -1), ...]"""
    alloc = []
    blocks = list(blocks)
    for ps in processes:
        placed = False
        for i, b in enumerate(blocks):
            if b >= ps:
                alloc.append((ps, i, b))
                blocks[i] -= ps
                placed = True
                break
        if not placed:
            alloc.append((ps, -1, 0))
    return alloc, blocks


def best_fit(blocks, processes):
    alloc = []
    blocks = list(blocks)
    for ps in processes:
        best_idx, best_size = -1, float('inf')
        for i, b in enumerate(blocks):
            if b >= ps and b < best_size:
                best_idx, best_size = i, b
        if best_idx != -1:
            alloc.append((ps, best_idx, blocks[best_idx]))
            blocks[best_idx] -= ps
        else:
            alloc.append((ps, -1, 0))
    return alloc, blocks


def worst_fit(blocks, processes):
    alloc = []
    blocks = list(blocks)
    for ps in processes:
        worst_idx, worst_size = -1, -1
        for i, b in enumerate(blocks):
            if b >= ps and b > worst_size:
                worst_idx, worst_size = i, b
        if worst_idx != -1:
            alloc.append((ps, worst_idx, blocks[worst_idx]))
            blocks[worst_idx] -= ps
        else:
            alloc.append((ps, -1, 0))
    return alloc, blocks


def next_fit(blocks, processes):
    alloc = []
    blocks = list(blocks)
    last = 0
    n = len(blocks)
    for ps in processes:
        placed = False
        for j in range(n):
            i = (last + j) % n
            if blocks[i] >= ps:
                alloc.append((ps, i, blocks[i]))
                blocks[i] -= ps
                last = i
                placed = True
                break
        if not placed:
            alloc.append((ps, -1, 0))
    return alloc, blocks


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE REPLACEMENT
# ═══════════════════════════════════════════════════════════════════════════════

def fifo_page_replacement(pages, frame_count):
    """FIFO page replacement. Returns (frames_over_time, faults, hits)."""
    frames = []
    queue = deque()
    history = []
    faults, hits = 0, 0
    for page in pages:
        if page in frames:
            hits += 1
            history.append((page, list(frames), False))
        else:
            faults += 1
            if len(frames) < frame_count:
                frames.append(page)
                queue.append(page)
            else:
                old = queue.popleft()
                frames[frames.index(old)] = page
                queue.append(page)
            history.append((page, list(frames), True))
    return history, faults, hits


def lru_page_replacement(pages, frame_count):
    """LRU page replacement."""
    frames = []
    history = []
    faults, hits = 0, 0
    recent = []
    for page in pages:
        if page in frames:
            hits += 1
            recent.remove(page)
            recent.append(page)
            history.append((page, list(frames), False))
        else:
            faults += 1
            if len(frames) < frame_count:
                frames.append(page)
            else:
                lru_page = recent.pop(0)
                frames[frames.index(lru_page)] = page
            recent.append(page)
            history.append((page, list(frames), True))
    return history, faults, hits


def optimal_page_replacement(pages, frame_count):
    """Optimal page replacement."""
    frames = []
    history = []
    faults, hits = 0, 0
    for idx, page in enumerate(pages):
        if page in frames:
            hits += 1
            history.append((page, list(frames), False))
        else:
            faults += 1
            if len(frames) < frame_count:
                frames.append(page)
            else:
                farthest = -1
                victim = 0
                for i, f in enumerate(frames):
                    try:
                        next_use = pages[idx + 1:].index(f)
                    except ValueError:
                        victim = i
                        break
                    if next_use > farthest:
                        farthest = next_use
                        victim = i
                frames[victim] = page
            history.append((page, list(frames), True))
    return history, faults, hits


# ═══════════════════════════════════════════════════════════════════════════════
# DEADLOCK — BANKER'S ALGORITHM
# ═══════════════════════════════════════════════════════════════════════════════

def bankers_algorithm(available, max_matrix, allocation_matrix):
    """
    Banker's Algorithm for deadlock avoidance.
    Returns (is_safe, safe_sequence, steps).
    """
    n = len(allocation_matrix)
    m = len(available)
    need = [[max_matrix[i][j] - allocation_matrix[i][j] for j in range(m)] for i in range(n)]
    work = list(available)
    finish = [False] * n
    safe_seq = []
    steps = []

    for _ in range(n):
        found = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                steps.append({
                    'process': i,
                    'work_before': list(work),
                    'need': list(need[i]),
                    'alloc': list(allocation_matrix[i]),
                })
                work = [work[j] + allocation_matrix[i][j] for j in range(m)]
                steps[-1]['work_after'] = list(work)
                finish[i] = True
                safe_seq.append(i)
                found = True
                break
        if not found:
            break

    return all(finish), safe_seq, steps


def deadlock_detection(available, allocation_matrix, request_matrix):
    """
    Deadlock Detection using wait-for graph approach.
    Returns (is_deadlocked, deadlocked_processes, safe_sequence).
    """
    n = len(allocation_matrix)
    m = len(available)
    work = list(available)
    finish = [False] * n

    # Mark processes with zero allocation as finished
    for i in range(n):
        if all(allocation_matrix[i][j] == 0 for j in range(m)):
            finish[i] = True

    safe_seq = []
    for _ in range(n):
        found = False
        for i in range(n):
            if not finish[i] and all(request_matrix[i][j] <= work[j] for j in range(m)):
                work = [work[j] + allocation_matrix[i][j] for j in range(m)]
                finish[i] = True
                safe_seq.append(i)
                found = True
                break
        if not found:
            break

    deadlocked = [i for i in range(n) if not finish[i]]
    return len(deadlocked) > 0, deadlocked, safe_seq


# ═══════════════════════════════════════════════════════════════════════════════
# DISK SCHEDULING
# ═══════════════════════════════════════════════════════════════════════════════

def disk_fcfs(requests, head):
    order = list(requests)
    seek = sum(abs(order[i] - (order[i-1] if i > 0 else head)) for i in range(len(order)))
    path = [head] + order
    return path, seek


def disk_sstf(requests, head):
    remaining = list(requests)
    path = [head]
    seek = 0
    current = head
    while remaining:
        closest = min(remaining, key=lambda x: abs(x - current))
        seek += abs(closest - current)
        current = closest
        path.append(current)
        remaining.remove(closest)
    return path, seek


def disk_scan(requests, head, disk_size=200, direction='right'):
    path = [head]
    seek = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    if direction == 'right':
        for r in right:
            seek += abs(r - path[-1])
            path.append(r)
        if right or True:
            seek += abs((disk_size - 1) - path[-1])
            path.append(disk_size - 1)
        for r in reversed(left):
            seek += abs(r - path[-1])
            path.append(r)
    else:
        for r in reversed(left):
            seek += abs(r - path[-1])
            path.append(r)
        seek += abs(0 - path[-1])
        path.append(0)
        for r in right:
            seek += abs(r - path[-1])
            path.append(r)
    return path, seek


def disk_cscan(requests, head, disk_size=200):
    path = [head]
    seek = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    for r in right:
        seek += abs(r - path[-1])
        path.append(r)
    seek += abs((disk_size - 1) - path[-1])
    path.append(disk_size - 1)
    seek += (disk_size - 1)
    path.append(0)
    for r in left:
        seek += abs(r - path[-1])
        path.append(r)
    return path, seek


def disk_look(requests, head, direction='right'):
    path = [head]
    seek = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    if direction == 'right':
        for r in right:
            seek += abs(r - path[-1])
            path.append(r)
        for r in reversed(left):
            seek += abs(r - path[-1])
            path.append(r)
    else:
        for r in reversed(left):
            seek += abs(r - path[-1])
            path.append(r)
        for r in right:
            seek += abs(r - path[-1])
            path.append(r)
    return path, seek


def disk_clook(requests, head):
    path = [head]
    seek = 0
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])

    for r in right:
        seek += abs(r - path[-1])
        path.append(r)
    if left:
        seek += abs(left[0] - path[-1])
        path.append(left[0])
        for r in left[1:]:
            seek += abs(r - path[-1])
            path.append(r)
    return path, seek


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY
# ═══════════════════════════════════════════════════════════════════════════════

def generate_random_processes(n, max_arrival=10, max_burst=10):
    return [(i+1, random.randint(0, max_arrival), random.randint(1, max_burst), random.randint(1, 3)) for i in range(n)]

def compare_cpu_algorithms(processes, quantum=2):
    """Run all CPU algorithms and return comparison data."""
    results = {}
    algos = {
        'FCFS': lambda: fcfs(processes),
        'SJF': lambda: sjf(processes),
        'SRTF': lambda: srtf(processes),
        'Round Robin': lambda: round_robin(processes, quantum),
        'Priority': lambda: priority_scheduling(processes),
        'MLFQ': lambda: mlfq(processes),
    }
    for name, func in algos.items():
        try:
            res, gantt = func()
            avg_wt = sum(r[3] for r in res) / len(res)
            avg_tat = sum(r[4] for r in res) / len(res)
            results[name] = {'result': res, 'gantt': gantt, 'avg_wt': avg_wt, 'avg_tat': avg_tat}
        except Exception:
            pass
    return results
