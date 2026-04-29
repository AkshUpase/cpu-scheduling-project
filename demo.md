# Live Demo Script (8–10 Minutes)

## 0:00–0:45 — Setup Pitch
- “This is an OS concepts simulator covering CPU scheduling, memory, deadlock, and disk scheduling.”
- “End-sem upgrade focus: interactive visualization + richer metrics + scenario-based learning.”

## 0:45–3:30 — CPU Scheduling (Core Differentiator)
1. Open CPU tab and load **Starvation preset**.
2. Run Priority without aging → show low-priority process waiting.
3. Enable aging preset/variant → rerun and compare.
4. Switch to Round Robin and show quantum impact.
5. Show metrics table: WT, TAT, RT, Throughput, CPU utilization, Context switches.

**Talking Point:** “Not just which algorithm is fast, but what overhead and fairness cost it introduces.”

## 3:30–5:00 — Animated Visualization Value
1. Play step-by-step timeline/Gantt.
2. Adjust speed.
3. Step forward (and backward if implemented).
4. Highlight process state changes.

**Talking Point:** “This bridges textbook theory with time-based execution behavior.”

## 5:00–6:15 — Disk Scheduling
1. Use same request queue on FCFS and LOOK.
2. Show seek path difference visually.
3. Mention head movement optimization and total seek distance.

## 6:15–7:15 — Deadlock
1. Run Banker’s safe case → safe sequence.
2. Run unsafe case / detection example.

**Talking Point:** “Shows practical safety checks before granting resources.”

## 7:15–8:00 — Memory
1. Show page replacement with FIFO vs LRU.
2. Explain Belady-like intuition in simple terms.

## 8:00–9:00 — End-Sem Delta Slide
- Mid-sem: algorithm execution + static outputs.
- End-sem: animations, presets, context-switch analytics, richer metrics, guided demos, report export.

## 9:00–10:00 — Q&A Buffer
- Keep 2-3 prepared benchmarks and one preset ready.

---

## Backup Plan (if feature incomplete)
- If animation is partial, use deterministic stepping with highlighted current tick.
- If aging toggle is incomplete, show two preset datasets representing before/after behavior.
- If PDF button incomplete, run report script manually and show generated file.
