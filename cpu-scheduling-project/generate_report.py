"""
OS Simulator Project — Detailed PDF Report Generator
Generates a comprehensive project explanation document.
"""
from fpdf import FPDF
import os

class ProjectReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "OS Simulator - Advanced Edition | Project Report", align="C")
        self.ln(4)
        self.set_draw_color(0, 212, 170)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def chapter_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(0, 100, 80)
        self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 212, 170)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 120, self.get_y())
        self.ln(6)

    def section_title(self, title):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def sub_section(self, title):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(80, 60, 140)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 5.5, text)
        self.ln(2)

    def bullet(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, text)

    def code_block(self, text):
        self.set_font("Courier", "", 9)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5, text, fill=True)
        self.ln(2)

    def add_table(self, headers, rows, col_widths=None):
        if col_widths is None:
            col_widths = [190 / len(headers)] * len(headers)
        # Header
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 170, 136)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_widths[i], 7, h, border=1, fill=True, align="C")
        self.ln()
        # Rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(30, 30, 30)
        fill = False
        for row in rows:
            if self.get_y() > 265:
                self.add_page()
            if fill:
                self.set_fill_color(245, 245, 245)
            else:
                self.set_fill_color(255, 255, 255)
            for i, val in enumerate(row):
                self.cell(col_widths[i], 6.5, str(val), border=1, fill=True, align="C")
            self.ln()
            fill = not fill
        self.ln(3)


def generate_report():
    pdf = ProjectReport()
    pdf.alias_nb_pages()

    # ══════════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(0, 100, 80)
    pdf.cell(0, 15, "OS Simulator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(100, 60, 180)
    pdf.cell(0, 12, "Advanced Edition", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_draw_color(0, 212, 170)
    pdf.set_line_width(1)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, "A Comprehensive Operating System Concepts Simulator", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "CPU Scheduling | Memory Management | Deadlock | Disk Scheduling", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 8, "Submitted By: Aksh Upase", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, "Second Year Engineering (SE)", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Subject: Operating Systems", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 7, "Built with: Python (CustomTkinter) + C", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "April 2026", align="C", new_x="LMARGIN", new_y="NEXT")

    # ══════════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("Table of Contents")
    toc = [
        "1. Introduction & Objectives",
        "2. Project Architecture & Technology Stack",
        "3. Module 1: CPU Scheduling Algorithms",
        "   3.1 FCFS (First Come First Served)",
        "   3.2 SJF (Shortest Job First)",
        "   3.3 SRTF (Shortest Remaining Time First)",
        "   3.4 Round Robin",
        "   3.5 Priority Scheduling",
        "   3.6 Multilevel Queue Scheduling",
        "   3.7 MLFQ (Multilevel Feedback Queue)",
        "4. Module 2: Memory Management",
        "   4.1 Memory Allocation (First/Best/Worst/Next Fit)",
        "   4.2 Page Replacement (FIFO, LRU, Optimal)",
        "5. Module 3: Deadlock Handling",
        "   5.1 Banker's Algorithm (Avoidance)",
        "   5.2 Deadlock Detection",
        "6. Module 4: Disk Scheduling",
        "   6.1 FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK",
        "7. UI Design & Features",
        "8. Algorithm Comparison & Analysis",
        "9. Conclusion & Learning Outcomes",
    ]
    for item in toc:
        pdf.set_font("Helvetica", "", 11 if not item.startswith("  ") else 10)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 6.5, item, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # ══════════════════════════════════════════════════════════════════════
    # 1. INTRODUCTION
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("1. Introduction & Objectives")
    pdf.body_text(
        "An Operating System (OS) is the core software that manages computer hardware and software resources. "
        "Understanding OS concepts like process scheduling, memory management, deadlock handling, and disk "
        "scheduling is fundamental to computer science and engineering education.\n\n"
        "This project is an interactive simulator that implements and visualizes 22+ OS algorithms across "
        "4 major modules. It provides a premium graphical user interface (GUI) with dark mode, Gantt charts, "
        "seek path visualizations, comparison modes, and auto-analysis capabilities."
    )
    pdf.section_title("Objectives")
    objectives = [
        "Implement and visualize major CPU scheduling algorithms including advanced ones like MLFQ.",
        "Simulate memory allocation strategies and page replacement algorithms with step-by-step display.",
        "Demonstrate deadlock avoidance using Banker's Algorithm with safe sequence computation.",
        "Implement and compare 6 disk scheduling algorithms with seek path visualization.",
        "Provide an intuitive, premium dark-themed GUI using CustomTkinter.",
        "Enable algorithm comparison with auto-analysis to identify the best algorithm.",
        "Support random test case generation and CSV export for academic documentation.",
        "Include a theory/learn section explaining each algorithm's pros and cons.",
    ]
    for obj in objectives:
        pdf.bullet(obj)
    pdf.ln(2)

    pdf.section_title("Scope of the Project")
    pdf.body_text(
        "The project covers 4 core OS modules:\n"
        "1) CPU Scheduling - 7 algorithms (FCFS, SJF, SRTF, RR, Priority, MLQ, MLFQ)\n"
        "2) Memory Management - 4 allocation + 3 page replacement algorithms\n"
        "3) Deadlock - Banker's Algorithm (avoidance) + Detection algorithm\n"
        "4) Disk Scheduling - 6 algorithms (FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK)\n\n"
        "Total: 22+ algorithm implementations with visual output."
    )

    # ══════════════════════════════════════════════════════════════════════
    # 2. ARCHITECTURE
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("2. Project Architecture & Technology Stack")

    pdf.section_title("Technology Stack")
    pdf.add_table(
        ["Component", "Technology", "Purpose"],
        [
            ["Backend (Original)", "C Language", "Core CPU scheduling algorithms"],
            ["Backend (Extended)", "Python 3", "All 22+ algorithm implementations"],
            ["GUI Framework", "CustomTkinter", "Premium dark-themed desktop UI"],
            ["Visualization", "Tkinter Canvas", "Gantt charts, seek paths, memory blocks"],
            ["Data Export", "CSV Module", "Export results to spreadsheet format"],
            ["Build System", "GCC / Makefile", "C code compilation"],
        ],
        [50, 50, 90]
    )

    pdf.section_title("Project Structure")
    pdf.code_block(
        "cpu-scheduling-project/\n"
        "|-- src/                    # C backend\n"
        "|   |-- main.c             # Entry point\n"
        "|   |-- fcfs.c             # FCFS algorithm\n"
        "|   |-- SJF.c              # SJF algorithm\n"
        "|   |-- round_robin.c      # Round Robin\n"
        "|   |-- priority_sch.c     # Priority Scheduling\n"
        "|   |-- input.c            # Input/Output functions\n"
        "|-- include/\n"
        "|   |-- scheduling.h       # Header declarations\n"
        "|-- ui/                    # Python GUI\n"
        "|   |-- app.py             # Main application entry\n"
        "|   |-- algorithms.py      # All algorithm implementations\n"
        "|   |-- tabs/\n"
        "|       |-- cpu_tab.py     # CPU Scheduling tab\n"
        "|       |-- memory_tab.py  # Memory Management tab\n"
        "|       |-- deadlock_tab.py# Deadlock tab\n"
        "|       |-- disk_tab.py    # Disk Scheduling tab\n"
        "|       |-- compare_tab.py # Comparison tab\n"
        "|       |-- learn_tab.py   # Theory section\n"
        "|-- output/                # Exported results\n"
        "|-- docs/                  # Documentation\n"
        "|-- scheduler.exe          # Compiled C binary"
    )

    pdf.section_title("Architecture Diagram")
    pdf.body_text(
        "The application follows a modular architecture:\n\n"
        "User Interface (app.py + CustomTkinter)\n"
        "    |-- CPU Tab --> algorithms.py (fcfs, sjf, srtf, rr, priority, mlq, mlfq)\n"
        "    |-- Memory Tab --> algorithms.py (first_fit, best_fit, worst_fit, next_fit,\n"
        "    |                                  fifo_page, lru_page, optimal_page)\n"
        "    |-- Deadlock Tab --> algorithms.py (bankers_algorithm, deadlock_detection)\n"
        "    |-- Disk Tab --> algorithms.py (disk_fcfs, sstf, scan, cscan, look, clook)\n"
        "    |-- Compare Tab --> algorithms.py (compare_cpu_algorithms)\n"
        "    |-- Learn Tab --> Static theory content\n\n"
        "Each tab is an independent module that imports algorithms from algorithms.py, "
        "ensuring clean separation of concerns between logic and presentation."
    )

    # ══════════════════════════════════════════════════════════════════════
    # 3. CPU SCHEDULING
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("3. Module 1: CPU Scheduling Algorithms")

    pdf.body_text(
        "CPU Scheduling determines the order in which processes are executed by the CPU. "
        "The goal is to optimize metrics like waiting time, turnaround time, and CPU utilization. "
        "This module implements 7 algorithms covering non-preemptive, preemptive, and multi-queue approaches."
    )

    # 3.1 FCFS
    pdf.section_title("3.1 FCFS (First Come First Served)")
    pdf.body_text(
        "FCFS is the simplest CPU scheduling algorithm. Processes are executed strictly in the "
        "order of their arrival time. It is non-preemptive - once a process starts executing, "
        "it runs to completion.\n\n"
        "Algorithm Steps:\n"
        "1. Sort processes by arrival time.\n"
        "2. Execute each process in order.\n"
        "3. If CPU is idle (no process has arrived), wait until next arrival.\n"
        "4. Calculate: Waiting Time = Start Time - Arrival Time\n"
        "5. Calculate: Turnaround Time = Waiting Time + Burst Time"
    )
    pdf.add_table(
        ["Aspect", "Detail"],
        [
            ["Type", "Non-Preemptive"],
            ["Complexity", "O(n)"],
            ["Advantage", "Simple, fair (FIFO order), no starvation"],
            ["Disadvantage", "Convoy effect - short jobs wait behind long ones"],
            ["Best For", "Batch processing systems"],
        ],
        [50, 140]
    )

    pdf.body_text("Example: Processes P1(AT=0,BT=5), P2(AT=1,BT=3), P3(AT=2,BT=8)")
    pdf.add_table(
        ["PID", "Arrival", "Burst", "Start", "Waiting", "Turnaround"],
        [["P1","0","5","0","0","5"], ["P2","1","3","5","4","7"], ["P3","2","8","8","6","14"]],
        [25, 30, 28, 28, 35, 44]
    )
    pdf.body_text("Average Waiting Time = (0+4+6)/3 = 3.33\nAverage Turnaround Time = (5+7+14)/3 = 8.67")

    # 3.2 SJF
    pdf.add_page()
    pdf.section_title("3.2 SJF (Shortest Job First)")
    pdf.body_text(
        "SJF selects the process with the smallest burst time among all arrived processes. "
        "It is non-preemptive and produces the optimal average waiting time for non-preemptive algorithms.\n\n"
        "Algorithm Steps:\n"
        "1. At each scheduling point, find all processes that have arrived.\n"
        "2. Select the one with the shortest burst time.\n"
        "3. Execute it completely (non-preemptive).\n"
        "4. Repeat until all processes are done."
    )
    pdf.add_table(
        ["Aspect", "Detail"],
        [
            ["Type", "Non-Preemptive"],
            ["Complexity", "O(n^2)"],
            ["Advantage", "Optimal average waiting time (non-preemptive)"],
            ["Disadvantage", "Starvation of long processes, requires burst prediction"],
            ["Best For", "When burst times are known in advance"],
        ],
        [50, 140]
    )

    # 3.3 SRTF
    pdf.section_title("3.3 SRTF (Shortest Remaining Time First)")
    pdf.body_text(
        "SRTF is the preemptive version of SJF. When a new process arrives with a burst time "
        "shorter than the remaining time of the currently running process, the CPU switches to "
        "the new process. This produces the optimal average waiting time among ALL algorithms.\n\n"
        "Algorithm Steps:\n"
        "1. At every time unit, check if a newly arrived process has shorter remaining time.\n"
        "2. If yes, preempt current process and switch.\n"
        "3. Track remaining burst time for each process.\n"
        "4. Process completes when remaining time reaches 0."
    )
    pdf.add_table(
        ["Aspect", "Detail"],
        [
            ["Type", "Preemptive"],
            ["Complexity", "O(n * total_time)"],
            ["Advantage", "Optimal average waiting time (overall best)"],
            ["Disadvantage", "High context-switch overhead, starvation possible"],
            ["Best For", "Time-sharing systems"],
        ],
        [50, 140]
    )

    # 3.4 Round Robin
    pdf.add_page()
    pdf.section_title("3.4 Round Robin (RR)")
    pdf.body_text(
        "Round Robin assigns a fixed time quantum to each process. Processes are placed in a "
        "circular queue. Each process runs for at most the quantum duration, then is moved to "
        "the back of the queue if not finished.\n\n"
        "Algorithm Steps:\n"
        "1. Maintain a ready queue (FIFO).\n"
        "2. Pick the front process.\n"
        "3. Run it for min(quantum, remaining_burst).\n"
        "4. If not finished, add it to the back of the queue.\n"
        "5. Enqueue any newly arrived processes.\n"
        "6. Repeat until all processes are done.\n\n"
        "Key Insight: Small quantum = better response time but more context switches. "
        "Large quantum = approaches FCFS behavior."
    )
    pdf.add_table(
        ["Aspect", "Detail"],
        [
            ["Type", "Preemptive"],
            ["Complexity", "O(n * total_time / quantum)"],
            ["Advantage", "Fair, good response time, no starvation"],
            ["Disadvantage", "Performance depends on quantum, context switch overhead"],
            ["Best For", "Interactive/time-sharing systems"],
        ],
        [50, 140]
    )

    # 3.5 Priority
    pdf.section_title("3.5 Priority Scheduling")
    pdf.body_text(
        "Each process is assigned a priority. The process with highest priority (lowest number) "
        "is selected for execution. This implementation is non-preemptive.\n\n"
        "Algorithm Steps:\n"
        "1. At each scheduling point, among arrived processes, pick the one with lowest priority number.\n"
        "2. Execute it completely.\n"
        "3. Tie-breaker: earlier arrival time.\n\n"
        "Problem: Low-priority processes may starve. Solution: Aging (increase priority over time)."
    )
    pdf.add_table(
        ["Aspect", "Detail"],
        [
            ["Type", "Non-Preemptive"],
            ["Advantage", "Important tasks are processed first"],
            ["Disadvantage", "Starvation of low-priority processes"],
            ["Solution", "Aging - gradually increase priority of waiting processes"],
        ],
        [50, 140]
    )

    # 3.6 MLQ
    pdf.add_page()
    pdf.section_title("3.6 Multilevel Queue Scheduling (MLQ)")
    pdf.body_text(
        "Multilevel Queue divides the ready queue into multiple separate queues, each with "
        "a different priority level and scheduling algorithm.\n\n"
        "In our implementation:\n"
        "- Queue 1 (Priority 1): System processes - uses FCFS (highest priority)\n"
        "- Queue 2 (Priority 2): Interactive processes - uses Round Robin\n"
        "- Queue 3 (Priority 3): Batch processes - uses FCFS (lowest priority)\n\n"
        "Processes are assigned to queues based on their priority value. Higher-priority queues "
        "are always served first. A process cannot move between queues.\n\n"
        "Advantage: Separates different types of processes for appropriate handling.\n"
        "Disadvantage: Inflexible - processes stuck in their queue; lower queues may starve."
    )

    # 3.7 MLFQ
    pdf.section_title("3.7 MLFQ (Multilevel Feedback Queue)")
    pdf.body_text(
        "MLFQ is the most sophisticated scheduling algorithm implemented in this project. "
        "Unlike MLQ, processes can MOVE between queues based on their behavior.\n\n"
        "Queue Structure:\n"
        "- Queue 1: Round Robin with small quantum (highest priority)\n"
        "- Queue 2: Round Robin with larger quantum\n"
        "- Queue 3: FCFS (lowest priority)\n\n"
        "Rules:\n"
        "1. New processes enter Queue 1 (highest priority).\n"
        "2. If a process uses its full quantum without completing, it is DEMOTED to the next queue.\n"
        "3. If a process completes within its quantum, it leaves the system.\n"
        "4. CPU-bound processes naturally sink to lower queues.\n"
        "5. I/O-bound processes stay in higher queues (they typically finish quickly).\n\n"
        "Why MLFQ is important:\n"
        "- It is ADAPTIVE - it learns process behavior without prior knowledge.\n"
        "- It approximates SJF without knowing burst times.\n"
        "- Most modern operating systems (Linux, Windows) use variants of MLFQ.\n"
        "- It provides good response time for short/interactive processes and reasonable throughput for long ones."
    )
    pdf.add_table(
        ["Aspect", "Detail"],
        [
            ["Type", "Preemptive, Multi-Queue, Adaptive"],
            ["Advantage", "Best of all worlds, adaptive to process behavior"],
            ["Disadvantage", "Complex to implement, requires tuning of parameters"],
            ["Used In", "Linux (CFS variant), Windows, macOS"],
        ],
        [50, 140]
    )

    # ══════════════════════════════════════════════════════════════════════
    # 4. MEMORY MANAGEMENT
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("4. Module 2: Memory Management")

    pdf.body_text(
        "Memory Management is responsible for allocating and deallocating memory to processes. "
        "This module covers two aspects: contiguous memory allocation strategies and virtual "
        "memory page replacement algorithms."
    )

    pdf.section_title("4.1 Memory Allocation Algorithms")
    pdf.body_text(
        "These algorithms decide which free memory block to allocate to a process. "
        "Given a list of memory blocks and process sizes, each algorithm uses a different strategy."
    )

    for name, desc, pros, cons in [
        ("First Fit",
         "Scans memory blocks from the beginning and allocates the FIRST block that is large enough.",
         "Fast - stops at first match, simple implementation",
         "Causes external fragmentation at the beginning of memory"),
        ("Best Fit",
         "Scans ALL blocks and allocates the SMALLEST block that is large enough.",
         "Minimizes wasted space within allocated block",
         "Slower (must scan all blocks), leaves tiny unusable fragments"),
        ("Worst Fit",
         "Scans ALL blocks and allocates the LARGEST available block.",
         "Leaves large remaining space that might be useful",
         "Wastes memory fastest, poor performance"),
        ("Next Fit",
         "Like First Fit, but starts searching from where the last allocation was made (wraps around).",
         "More even distribution of allocations across memory",
         "May miss better-fitting blocks earlier in memory"),
    ]:
        pdf.sub_section(name)
        pdf.body_text(f"{desc}\n\nAdvantage: {pros}\nDisadvantage: {cons}")

    pdf.add_page()
    pdf.section_title("4.2 Page Replacement Algorithms")
    pdf.body_text(
        "When a page fault occurs and all frames are full, the OS must choose a page to evict. "
        "Page replacement algorithms determine which page to remove.\n\n"
        "Input: A reference string (sequence of page requests) and number of frames.\n"
        "Output: Number of page faults, hits, and frame state at each step."
    )

    pdf.sub_section("FIFO (First In First Out)")
    pdf.body_text(
        "Replaces the page that was loaded into memory FIRST (oldest page).\n\n"
        "Implementation: Uses a queue. When a fault occurs and frames are full, remove "
        "the front of the queue and add the new page to the back.\n\n"
        "Advantage: Simple to implement.\n"
        "Disadvantage: Suffers from Belady's Anomaly - more frames can cause MORE faults."
    )

    pdf.sub_section("LRU (Least Recently Used)")
    pdf.body_text(
        "Replaces the page that has not been used for the LONGEST time.\n\n"
        "Implementation: Track the order of page accesses. On a fault, evict the page "
        "whose last access was furthest in the past.\n\n"
        "Advantage: Good performance, does NOT suffer from Belady's Anomaly.\n"
        "Disadvantage: Expensive to implement perfectly (requires hardware support or complex tracking).\n\n"
        "LRU is the most commonly used page replacement algorithm in practice."
    )

    pdf.sub_section("Optimal (OPT)")
    pdf.body_text(
        "Replaces the page that will NOT be used for the LONGEST time in the future.\n\n"
        "Implementation: For each page in frames, find its next occurrence in the reference "
        "string. Evict the one with the farthest (or no) future use.\n\n"
        "Advantage: Produces the minimum number of page faults (theoretical best).\n"
        "Disadvantage: IMPOSSIBLE to implement in practice - requires future knowledge. "
        "Used only as a benchmark to evaluate other algorithms."
    )

    pdf.body_text("Example: Reference String = 7,0,1,2,0,3,0,4,2,3,0,3,2 with 3 frames")
    pdf.add_table(
        ["Algorithm", "Page Faults", "Page Hits", "Hit Ratio"],
        [
            ["FIFO", "10", "3", "23.1%"],
            ["LRU", "10", "3", "23.1%"],
            ["Optimal", "9", "4", "30.8%"],
        ],
        [45, 45, 45, 45]
    )

    # ══════════════════════════════════════════════════════════════════════
    # 5. DEADLOCK
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("5. Module 3: Deadlock Handling")

    pdf.body_text(
        "A deadlock occurs when a set of processes are waiting for resources held by each other, "
        "creating a circular dependency. No process can proceed.\n\n"
        "Four Necessary Conditions for Deadlock (all must hold simultaneously):\n"
        "1. Mutual Exclusion - Resources cannot be shared.\n"
        "2. Hold and Wait - Process holds resources while waiting for others.\n"
        "3. No Preemption - Resources cannot be forcibly taken.\n"
        "4. Circular Wait - Circular chain of processes waiting for each other."
    )

    pdf.section_title("5.1 Banker's Algorithm (Deadlock Avoidance)")
    pdf.body_text(
        "The Banker's Algorithm determines whether granting a resource request will leave "
        "the system in a SAFE STATE. A safe state means there exists at least one sequence "
        "in which all processes can complete.\n\n"
        "Inputs:\n"
        "- Available: Vector of currently available resources of each type\n"
        "- Max: Matrix of maximum resource demands per process\n"
        "- Allocation: Matrix of currently allocated resources per process\n"
        "- Need = Max - Allocation (what each process still needs)\n\n"
        "Safety Algorithm Steps:\n"
        "1. Initialize Work = Available, Finish[i] = false for all i.\n"
        "2. Find process i such that Finish[i] == false AND Need[i] <= Work.\n"
        "3. If found: Work = Work + Allocation[i], Finish[i] = true. Go to step 2.\n"
        "4. If not found: If all Finish[i] == true, system is SAFE. Else, UNSAFE (deadlock possible).\n\n"
        "The safe sequence shows the order in which processes can complete."
    )

    pdf.body_text("Example with 5 processes and 3 resource types:")
    pdf.add_table(
        ["Process", "Allocation", "Max", "Need", "Available"],
        [
            ["P0", "0 1 0", "7 5 3", "7 4 3", "3 3 2"],
            ["P1", "2 0 0", "3 2 2", "1 2 2", ""],
            ["P2", "3 0 2", "9 0 2", "6 0 0", ""],
            ["P3", "2 1 1", "2 2 2", "0 1 1", ""],
            ["P4", "0 0 2", "4 3 3", "4 3 1", ""],
        ],
        [30, 40, 35, 35, 40]
    )
    pdf.body_text("Safe Sequence: P1 -> P3 -> P4 -> P0 -> P2 (System is SAFE)")

    pdf.section_title("5.2 Deadlock Detection")
    pdf.body_text(
        "Unlike avoidance, detection allows deadlocks to occur and then identifies them.\n\n"
        "Algorithm:\n"
        "1. Initialize Work = Available.\n"
        "2. Find process i with Request[i] <= Work.\n"
        "3. If found: Work = Work + Allocation[i] (assume it finishes). Repeat.\n"
        "4. Processes not found are DEADLOCKED.\n\n"
        "Recovery options: Kill deadlocked processes, rollback, or preempt resources."
    )

    # ══════════════════════════════════════════════════════════════════════
    # 6. DISK SCHEDULING
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("6. Module 4: Disk Scheduling")

    pdf.body_text(
        "Disk scheduling algorithms determine the order in which disk I/O requests are serviced. "
        "The goal is to minimize total seek time (head movement). The metric used is Total Seek Time "
        "= sum of absolute differences between consecutive head positions."
    )

    algos = [
        ("FCFS", "Services requests in the order they arrive.",
         "Fair, simple", "Can result in large seek times"),
        ("SSTF (Shortest Seek Time First)", "Always services the request closest to the current head position.",
         "Low average seek time", "Starvation of far requests"),
        ("SCAN (Elevator Algorithm)", "Head moves in one direction servicing all requests, then reverses direction. Goes to the end of the disk.",
         "No starvation, good throughput", "Requests at edges may wait longer"),
        ("C-SCAN (Circular SCAN)", "Like SCAN but only services in one direction. When reaching the end, jumps back to the start.",
         "More uniform waiting time", "Empty return sweep wastes time"),
        ("LOOK", "Like SCAN but only goes as far as the farthest request (not the disk edge).",
         "More efficient than SCAN", "Slight unfairness at edges"),
        ("C-LOOK", "Like C-SCAN but only goes as far as the farthest request in each direction.",
         "Best overall performance in most cases", "Slightly more complex"),
    ]
    for name, desc, pros, cons in algos:
        pdf.sub_section(name)
        pdf.body_text(f"{desc}\n\nAdvantage: {pros}\nDisadvantage: {cons}")

    pdf.body_text("\nExample: Request queue = 98,183,37,122,14,124,65,67 | Head = 53 | Disk size = 200")
    pdf.add_table(
        ["Algorithm", "Total Seek Time", "Efficiency"],
        [
            ["FCFS", "640", "Baseline"],
            ["SSTF", "236", "Good"],
            ["SCAN", "331", "Fair"],
            ["C-SCAN", "382", "Uniform"],
            ["LOOK", "299", "Better"],
            ["C-LOOK", "322", "Good"],
        ],
        [50, 60, 80]
    )
    pdf.body_text("(Actual seek times vary based on request ordering and head position)")

    # ══════════════════════════════════════════════════════════════════════
    # 7. UI DESIGN
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("7. UI Design & Features")

    pdf.body_text(
        "The application uses CustomTkinter (built on top of Tkinter) to create a modern, "
        "dark-themed desktop GUI with 6 tabs."
    )

    pdf.section_title("Design Principles")
    for p in [
        "Dark Mode: Background #0d1117, panels #161b22, cards #1c2230 - reduces eye strain.",
        "Accent Colors: Teal (#00d4aa) for primary, Purple (#7c3aed) for secondary highlights.",
        "Monospace Font (Consolas): Used throughout for consistency and code-like appearance.",
        "Modular Tabs: Each OS module has its own tab for clean separation.",
        "Responsive Layout: Left panel for controls, right panel for results.",
    ]:
        pdf.bullet(p)

    pdf.ln(3)
    pdf.section_title("Tab Overview")
    pdf.add_table(
        ["Tab", "Features"],
        [
            ["CPU Scheduling", "7 algorithms, Gantt chart, stats cards, auto-analysis, CSV export"],
            ["Memory", "4 allocation + 3 page replacement, block visualization, step-by-step table"],
            ["Deadlock", "Banker's Algorithm (step-by-step) + Deadlock Detection"],
            ["Disk Scheduling", "6 algorithms, seek path visualization, compare-all mode"],
            ["Compare All", "Run all CPU algorithms on same data, bar charts, best/worst analysis"],
            ["Learn", "Theory section with explanation and pros/cons for every algorithm"],
        ],
        [40, 150]
    )

    pdf.section_title("Key UI Features")
    features = [
        "Gantt Chart Canvas: Visual timeline showing process execution order with color-coded bars.",
        "Random Test Case Generator: One-click generation of random process data for testing.",
        "Algorithm Comparison Mode: Side-by-side bar charts comparing avg WT and TAT.",
        "Auto-Analysis: Automatically identifies and recommends the best performing algorithm.",
        "CSV Export: Save simulation results to CSV files for further analysis.",
        "Step-by-Step Display: Banker's Algorithm shows each step of the safety check.",
        "Seek Path Visualization: Interactive graph showing disk head movement path.",
        "Theory Section: Built-in reference for every algorithm with pros and cons.",
    ]
    for f in features:
        pdf.bullet(f)

    # ══════════════════════════════════════════════════════════════════════
    # 8. COMPARISON
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("8. Algorithm Comparison & Analysis")

    pdf.section_title("CPU Scheduling Comparison")
    pdf.add_table(
        ["Algorithm", "Type", "Optimal WT?", "Starvation?", "Complexity"],
        [
            ["FCFS", "Non-Preemptive", "No", "No", "O(n)"],
            ["SJF", "Non-Preemptive", "Yes (NP)", "Yes", "O(n^2)"],
            ["SRTF", "Preemptive", "Yes (all)", "Yes", "O(n*T)"],
            ["Round Robin", "Preemptive", "No", "No", "O(n*T/q)"],
            ["Priority", "Non-Preemptive", "No", "Yes (fixable)", "O(n^2)"],
            ["MLQ", "Multi-Queue", "No", "Yes", "O(n^2)"],
            ["MLFQ", "Adaptive", "Approximates", "No", "O(n*T)"],
        ],
        [35, 35, 30, 32, 38]
    )

    pdf.section_title("Page Replacement Comparison")
    pdf.add_table(
        ["Algorithm", "Belady's Anomaly?", "Performance", "Practical?"],
        [
            ["FIFO", "Yes", "Average", "Yes"],
            ["LRU", "No", "Good", "Yes (with hardware)"],
            ["Optimal", "No", "Best (theoretical)", "No (needs future)"],
        ],
        [40, 45, 45, 50]
    )

    pdf.section_title("Disk Scheduling Comparison")
    pdf.add_table(
        ["Algorithm", "Starvation?", "Seek Time", "Uniformity"],
        [
            ["FCFS", "No", "High", "Low"],
            ["SSTF", "Yes", "Low", "Low"],
            ["SCAN", "No", "Medium", "Medium"],
            ["C-SCAN", "No", "Medium", "High"],
            ["LOOK", "No", "Low-Medium", "Medium"],
            ["C-LOOK", "No", "Low", "High"],
        ],
        [40, 40, 45, 45]
    )

    # ══════════════════════════════════════════════════════════════════════
    # 9. CONCLUSION
    # ══════════════════════════════════════════════════════════════════════
    pdf.add_page()
    pdf.chapter_title("9. Conclusion & Learning Outcomes")

    pdf.body_text(
        "This project provides a comprehensive, hands-on understanding of core Operating System "
        "concepts through interactive simulation and visualization. By implementing 22+ algorithms "
        "across 4 major OS modules, the project demonstrates both theoretical knowledge and "
        "practical programming skills."
    )

    pdf.section_title("Key Learning Outcomes")
    outcomes = [
        "Understanding of process scheduling trade-offs (waiting time vs. response time vs. fairness).",
        "Practical implementation of advanced algorithms like MLFQ used in real operating systems.",
        "Comprehension of memory management challenges (fragmentation, page faults).",
        "Ability to detect and avoid deadlocks using Banker's Algorithm.",
        "Knowledge of disk scheduling optimizations for reducing seek time.",
        "GUI development skills using modern Python frameworks.",
        "Software architecture principles (modular design, separation of concerns).",
    ]
    for o in outcomes:
        pdf.bullet(o)

    pdf.ln(4)
    pdf.section_title("Key Takeaways")
    pdf.body_text(
        "1. MLFQ is the most practical CPU scheduling algorithm - it adapts to process behavior "
        "without prior knowledge and is used in Linux, Windows, and macOS.\n\n"
        "2. LRU is the most practical page replacement algorithm - it provides good performance "
        "without needing future knowledge (unlike Optimal).\n\n"
        "3. Banker's Algorithm prevents deadlocks proactively but requires processes to declare "
        "maximum resource needs upfront.\n\n"
        "4. C-LOOK generally provides the best disk scheduling performance with uniform wait times.\n\n"
        "5. No single algorithm is best for all scenarios - the choice depends on workload, "
        "system requirements, and trade-offs between metrics."
    )

    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(0, 100, 80)
    pdf.cell(0, 10, "--- End of Report ---", align="C")

    # ══════════════════════════════════════════════════════════════════════
    # SAVE
    # ══════════════════════════════════════════════════════════════════════
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "OS_Project_Report.pdf")
    pdf.output(output_path)
    print(f"\nPDF Generated Successfully!")
    print(f"Location: {output_path}")
    print(f"Pages: {pdf.page_no()}")
    return output_path


# ═══════════════════════════════════════════════════════════════════════════════
# PER-SIMULATION REPORT  (called from the UI's "Export PDF" button)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_simulation_report(result, processes, gantt, stats, output_path):
    """
    Generate a concise PDF for a single simulation run.

    Parameters
    ----------
    result      : list of (pid, arrival, burst, waiting, turnaround)
    processes   : list of (pid, arrival, burst, priority)
    gantt       : list of (pid, start, end) — the Gantt chart segments
    stats       : dict with keys: algo, avg_wt, avg_tat,
                  context_switches, cpu_util, throughput
    output_path : str — destination file path
    """
    pdf = ProjectReport()
    pdf.alias_nb_pages()
    pdf.add_page()

    # ── Title ─────────────────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(0, 100, 80)
    pdf.cell(0, 12, "CPU Scheduling - Simulation Report",
             new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("Helvetica", "", 13)
    pdf.set_text_color(100, 60, 180)
    algo_display = stats.get("algo", "").upper()
    pdf.cell(0, 8, f"Algorithm: {algo_display}",
             new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)
    pdf.set_draw_color(0, 212, 170)
    pdf.set_line_width(0.8)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(6)

    # ── Metrics summary ───────────────────────────────────────────────────────
    pdf.chapter_title("Performance Metrics")
    metrics = [
        ["Average Waiting Time",    f"{stats.get('avg_wt', 0):.2f}  units"],
        ["Average Turnaround Time", f"{stats.get('avg_tat', 0):.2f}  units"],
        ["CPU Utilization",         f"{stats.get('cpu_util', 0):.1f} %"],
        ["Context Switches",        str(stats.get('context_switches', 0))],
        ["Throughput",              f"{stats.get('throughput', 0)} processes/unit"],
    ]
    pdf.add_table(["Metric", "Value"], metrics, [120, 70])

    # ── Input processes ───────────────────────────────────────────────────────
    pdf.chapter_title("Input Processes")
    proc_rows = [[f"P{p[0]}", p[1], p[2], p[3]] for p in processes]
    pdf.add_table(["PID", "Arrival", "Burst", "Priority"], proc_rows,
                  [40, 50, 50, 50])

    # ── Results table ─────────────────────────────────────────────────────────
    pdf.chapter_title("Scheduling Results")
    res_rows = []
    for r in result:
        pid, at, bt, wt, tat = r
        rt_ratio = f"{tat / bt:.2f}" if bt else "–"
        res_rows.append([f"P{pid}", at, bt, wt, tat, rt_ratio])
    pdf.add_table(
        ["PID", "Arrival", "Burst", "Waiting", "Turnaround", "Resp Ratio"],
        res_rows,
        [30, 32, 32, 32, 38, 36],
    )

    # ── Gantt chart (text representation) ────────────────────────────────────
    pdf.chapter_title("Gantt Chart (text)")
    pdf.set_font("Courier", "", 8)
    pdf.set_text_color(30, 30, 30)
    # Draw each block as a cell to avoid word-wrap issues
    cell_w = 18
    for pid, start, end in gantt:
        label = f"P{pid}({start}-{end})"
        pdf.cell(cell_w, 6, label[:cell_w], border=1, align="C")
    pdf.ln(8)
    pdf.ln(4)

    # ── Analysis note ──────────────────────────────────────────────────────────
    pdf.chapter_title("Analysis")
    if result:
        best_p  = min(result, key=lambda r: r[3])
        worst_p = max(result, key=lambda r: r[3])
        analysis = (
            f"Algorithm '{algo_display}' scheduled {len(result)} processes. "
            f"Best waiting time: P{best_p[0]} ({best_p[3]} units). "
            f"Worst waiting time: P{worst_p[0]} ({worst_p[3]} units). "
            f"Context switches: {stats.get('context_switches', 0)} "
            f"(lower = less overhead). "
            f"CPU utilization: {stats.get('cpu_util', 0):.1f}% "
            f"(higher = more efficient). "
            f"Throughput: {stats.get('throughput', 0)} processes per time unit."
        )
        pdf.body_text(analysis)

    pdf.output(output_path)
    return output_path


if __name__ == "__main__":
    generate_report()
