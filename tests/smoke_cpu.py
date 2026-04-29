"""Offline smoke checks for CPU scheduling analytics.
Run: python tests/smoke_cpu.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cpu-scheduling-project", "ui"))

from algorithms import (
    fcfs, sjf, srtf, round_robin, priority_scheduling, mlfq,
    compare_cpu_algorithms, throughput_vs_quantum, response_times, context_switches,
)


def main():
    procs = [(1, 0, 5, 2), (2, 1, 3, 1), (3, 2, 2, 3), (4, 3, 1, 2)]

    for fn in [fcfs, sjf, srtf, priority_scheduling, mlfq]:
        res, gantt = fn(procs)
        assert len(res) == len(procs), f"{fn.__name__}: missing process result"
        assert gantt, f"{fn.__name__}: empty gantt"
        assert context_switches(gantt) >= 0

    rr_res, rr_gantt = round_robin(procs, 2)
    assert len(rr_res) == len(procs)
    assert rr_gantt

    rt = response_times(procs, rr_gantt)
    assert set(rt.keys()) == {1, 2, 3, 4}

    cmp = compare_cpu_algorithms(procs, quantum=2)
    assert cmp, "comparison returned empty"
    for name, data in cmp.items():
        if data.get("error"):
            continue
        for key in ["avg_wt", "avg_tat", "avg_rt", "context_switches", "throughput", "cpu_util"]:
            assert key in data, f"{name}: missing {key}"

    rr_curve = throughput_vs_quantum(procs, range(1, 6))
    valid = [x for x in rr_curve if x[1] is not None]
    assert valid, "no valid rr quantum points"

    print("smoke_cpu: OK")


if __name__ == "__main__":
    main()
