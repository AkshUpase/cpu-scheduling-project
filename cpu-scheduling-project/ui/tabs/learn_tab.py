"""Learn Tab — Theory section explaining each algorithm with pros/cons."""
import customtkinter as ctk

ACCENT="#00d4aa"; BG="#0d1117"; PANEL="#161b22"; CARD="#1c2230"
BORDER="#30363d"; TEXT="#e6edf3"; SUBTEXT="#8b949e"

TOPICS = {
    "🧠 CPU Scheduling": [
        ("FCFS — First Come First Served",
         "Processes executed in arrival order. Non-preemptive.",
         "✅ Simple, fair\n❌ Convoy effect, high avg WT for short jobs"),
        ("SJF — Shortest Job First",
         "Selects process with smallest burst time. Non-preemptive.",
         "✅ Optimal avg WT for non-preemptive\n❌ Starvation of long processes, needs burst prediction"),
        ("SRTF — Shortest Remaining Time First",
         "Preemptive version of SJF. Running process can be interrupted.",
         "✅ Optimal avg WT overall\n❌ High context-switch overhead, starvation possible"),
        ("Round Robin",
         "Each process gets a fixed time quantum. Preemptive, circular queue.",
         "✅ Fair, good response time\n❌ Performance depends on quantum, high context switches"),
        ("Priority Scheduling",
         "Process with highest priority (lowest number) executes first.",
         "✅ Important tasks first\n❌ Starvation (solved by aging)"),
        ("Multilevel Queue",
         "Multiple queues with different priorities. Each queue has its own algorithm.",
         "✅ Flexible, separates process types\n❌ Starvation of lower queues, inflexible"),
        ("MLFQ — Multilevel Feedback Queue ⭐",
         "Processes move between queues based on behavior. CPU-bound demoted, I/O-bound promoted.",
         "✅ Adaptive, best of all worlds\n❌ Complex to implement, needs tuning"),
    ],
    "💾 Memory Management": [
        ("First Fit", "Allocates first block that's big enough.", "✅ Fast\n❌ External fragmentation"),
        ("Best Fit", "Allocates smallest sufficient block.", "✅ Minimizes wasted space\n❌ Slower, leaves tiny fragments"),
        ("Worst Fit", "Allocates largest available block.", "✅ Leaves large remaining space\n❌ Wastes memory quickly"),
        ("Next Fit", "Like First Fit, but starts from last allocation.", "✅ Even distribution\n❌ May miss better fits"),
        ("FIFO Page Replacement", "Replaces oldest page in memory.", "✅ Simple\n❌ Belady's anomaly"),
        ("LRU Page Replacement ⭐", "Replaces least recently used page.", "✅ Good performance, no Belady's\n❌ Expensive to implement perfectly"),
        ("Optimal Page Replacement ⭐", "Replaces page not needed for longest time.", "✅ Minimum faults (theoretical best)\n❌ Requires future knowledge"),
    ],
    "⚠️ Deadlock": [
        ("Deadlock Conditions", "Mutual Exclusion + Hold & Wait + No Preemption + Circular Wait.",
         "All 4 conditions must hold simultaneously for deadlock."),
        ("Banker's Algorithm ⭐", "Checks if resource allocation leads to safe state before granting.",
         "✅ Prevents deadlock\n❌ Requires max resource declaration, conservative"),
        ("Deadlock Detection", "Periodically checks for circular wait in resource allocation graph.",
         "✅ No prevention overhead\n❌ Recovery is expensive (kill/rollback)"),
    ],
    "💽 Disk Scheduling": [
        ("FCFS", "Services requests in arrival order.", "✅ Fair\n❌ Long seek times"),
        ("SSTF", "Services nearest request first.", "✅ Low seek time\n❌ Starvation of far requests"),
        ("SCAN (Elevator)", "Head moves in one direction servicing all requests, then reverses.",
         "✅ No starvation\n❌ Requests at edges wait longer"),
        ("C-SCAN", "Like SCAN but only services in one direction, jumps back to start.",
         "✅ More uniform wait time\n❌ Empty return sweep wastes time"),
    ],
}

class LearnTab:
    def __init__(self, parent):
        self.parent = parent
        self._build()

    def _build(self):
        main = ctk.CTkFrame(self.parent, fg_color=BG)
        main.pack(fill="both", expand=True)

        ctk.CTkLabel(main, text="📚 LEARN OS CONCEPTS",
                     font=ctk.CTkFont("Consolas",16,"bold"), text_color=ACCENT).pack(pady=(12,4))
        ctk.CTkLabel(main, text="Click a topic to expand. Master these for your exam!",
                     font=ctk.CTkFont("Consolas",10), text_color=SUBTEXT).pack(pady=(0,8))

        scroll = ctk.CTkScrollableFrame(main, fg_color=BG)
        scroll.pack(fill="both", expand=True, padx=16, pady=(0,12))

        for section, items in TOPICS.items():
            sec_frame = ctk.CTkFrame(scroll, fg_color=PANEL, corner_radius=8)
            sec_frame.pack(fill="x", pady=(8,0))
            ctk.CTkLabel(sec_frame, text=section, font=ctk.CTkFont("Consolas",13,"bold"),
                         text_color=ACCENT).pack(anchor="w", padx=16, pady=(10,6))

            for title, desc, pros_cons in items:
                card = ctk.CTkFrame(sec_frame, fg_color=CARD, corner_radius=6)
                card.pack(fill="x", padx=12, pady=3)
                ctk.CTkLabel(card, text=f"  {title}",
                             font=ctk.CTkFont("Consolas",11,"bold"),
                             text_color="#f59e0b").pack(anchor="w", padx=8, pady=(6,0))
                ctk.CTkLabel(card, text=f"  {desc}",
                             font=ctk.CTkFont("Consolas",9),
                             text_color=TEXT, wraplength=700, justify="left").pack(anchor="w", padx=8, pady=2)
                ctk.CTkLabel(card, text=f"  {pros_cons}",
                             font=ctk.CTkFont("Consolas",9),
                             text_color="#4ade80", wraplength=700, justify="left").pack(anchor="w", padx=8, pady=(0,6))

            # padding at bottom
            ctk.CTkFrame(sec_frame, fg_color=PANEL, height=6).pack()
