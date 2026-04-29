"""CPU Scheduling Tab — FCFS, SJF, SRTF, RR, Priority, MLQ, MLFQ.

Showcase features
-----------------
* Animated / step-by-step Gantt chart with speed slider
* Process state timeline diagram
* Context-switch counter + throughput in stats cards
* Response-time column in results table
* Aging toggle for Priority scheduling (anti-starvation demo)
* Round Robin — WT vs Quantum analysis chart
* Preset scenarios (Convoy Effect, Starvation, Optimal, I/O Bound)
* Save / Load process configurations as JSON
* Export results as CSV  or  PDF report
"""
import customtkinter as ctk
from tkinter import messagebox, filedialog, Canvas
import random, csv, os, sys, json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms import (
    fcfs, sjf, srtf, round_robin, priority_scheduling,
    multilevel_queue, mlfq, generate_random_processes,
    context_switches, response_times,
    priority_scheduling_aging, throughput_vs_quantum,
)

ACCENT = "#00d4aa"; ACCENT2 = "#7c3aed"; BG = "#0d1117"; PANEL = "#161b22"
CARD   = "#1c2230"; BORDER = "#30363d"; TEXT = "#e6edf3"; SUBTEXT = "#8b949e"
COLORS = ["#00d4aa", "#7c3aed", "#f59e0b", "#f87171",
          "#4ade80", "#60a5fa", "#f472b6", "#fb923c", "#34d399", "#a78bfa"]

# ── Preset scenarios ───────────────────────────────────────────────────────────
PRESETS = {
    "Convoy":    [(1, 0, 24, 2), (2, 1, 3, 1), (3, 2, 3, 1)],
    "Starvation": [(1, 0, 2, 1), (2, 0, 2, 1), (3, 0, 2, 1),
                   (4, 0, 8, 3), (5, 1, 4, 3)],
    "Optimal":   [(1, 0, 4, 2), (2, 1, 3, 1), (3, 2, 1, 1),
                  (4, 3, 2, 2), (5, 4, 5, 3)],
    "I/O Bound": [(1, 0, 1, 1), (2, 0, 8, 3), (3, 1, 1, 1),
                  (4, 2, 1, 2), (5, 3, 7, 3), (6, 4, 1, 1)],
}

ALGO_LABELS = {
    "fcfs": "FCFS",
    "sjf":  "SJF (Non-Preemptive)",
    "srtf": "SRTF (Preemptive)",
    "rr":   "Round Robin",
    "pri":  "Priority",
    "mlq":  "Multilevel Queue",
    "mlfq": "MLFQ ⭐",
}


class CPUTab:
    def __init__(self, parent):
        self.parent      = parent
        self.rows        = []
        self.gantt_data  = []
        self.last_result = None
        self._last_procs = []
        self._aging_log  = []
        self._anim_step  = 0
        self._anim_id    = None
        self._build()

    # ════════════════════════════════════════════════════════════════════════════
    # UI CONSTRUCTION
    # ════════════════════════════════════════════════════════════════════════════

    def _build(self):
        main = ctk.CTkFrame(self.parent, fg_color=BG)
        main.pack(fill="both", expand=True)
        self._build_left(main)
        self._build_right(main)

    # ── Left panel ─────────────────────────────────────────────────────────────
    def _build_left(self, main):
        left = ctk.CTkFrame(main, fg_color=PANEL, width=310, corner_radius=0)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        # Algorithm selector
        ctk.CTkLabel(left, text="ALGORITHM",
                     font=ctk.CTkFont("Consolas", 11, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(12, 4))
        self.algo_var = ctk.StringVar(value="fcfs")
        for val, label in ALGO_LABELS.items():
            ctk.CTkRadioButton(
                left, text=label, variable=self.algo_var, value=val,
                font=ctk.CTkFont("Consolas", 11), text_color=TEXT,
                fg_color=ACCENT, hover_color=ACCENT2,
                command=self._on_algo_change,
            ).pack(anchor="w", padx=20, pady=2)

        # Quantum entry (shown for rr / mlfq)
        self.q_frame = ctk.CTkFrame(left, fg_color=PANEL)
        ctk.CTkLabel(self.q_frame, text="Quantum:",
                     font=ctk.CTkFont("Consolas", 11),
                     text_color=SUBTEXT).pack(side="left", padx=(0, 8))
        self.q_entry = ctk.CTkEntry(self.q_frame, width=50,
                                    font=ctk.CTkFont("Consolas", 11))
        self.q_entry.insert(0, "2")
        self.q_entry.pack(side="left")

        # Aging toggle (shown for priority)
        self.aging_frame = ctk.CTkFrame(left, fg_color=PANEL)
        self.aging_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            self.aging_frame,
            text="⏫ Enable Aging (anti-starvation)",
            variable=self.aging_var,
            font=ctk.CTkFont("Consolas", 10), text_color="#f59e0b",
            fg_color=ACCENT, hover_color=ACCENT2, checkmark_color=BG,
        ).pack(side="left", padx=4, pady=4)

        # Divider + process table controls
        ctk.CTkFrame(left, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(left, text="PROCESSES",
                     font=ctk.CTkFont("Consolas", 11, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(0, 4))

        ctrl = ctk.CTkFrame(left, fg_color=PANEL)
        ctrl.pack(fill="x", padx=16, pady=2)
        ctk.CTkLabel(ctrl, text="Count:",
                     font=ctk.CTkFont("Consolas", 11),
                     text_color=SUBTEXT).pack(side="left")
        self.n_entry = ctk.CTkEntry(ctrl, width=38,
                                    font=ctk.CTkFont("Consolas", 11))
        self.n_entry.insert(0, "5")
        self.n_entry.pack(side="left", padx=6)
        ctk.CTkButton(ctrl, text="Generate", width=68, fg_color=ACCENT2,
                      hover_color="#6d28d9",
                      font=ctk.CTkFont("Consolas", 10),
                      command=self._gen).pack(side="left", padx=2)
        ctk.CTkButton(ctrl, text="🎲 Rnd", width=60, fg_color="#f59e0b",
                      hover_color="#d97706", text_color=BG,
                      font=ctk.CTkFont("Consolas", 10),
                      command=self._random).pack(side="left", padx=2)

        # Table header
        hdr = ctk.CTkFrame(left, fg_color=CARD, corner_radius=4)
        hdr.pack(fill="x", padx=16, pady=(6, 0))
        for col in ["PID", "AT", "BT", "Pri"]:
            ctk.CTkLabel(hdr, text=col,
                         font=ctk.CTkFont("Consolas", 9, "bold"),
                         text_color=SUBTEXT, width=38).pack(side="left", padx=4, pady=4)

        self.proc_scroll = ctk.CTkScrollableFrame(left, fg_color=PANEL, height=130)
        self.proc_scroll.pack(fill="x", padx=16, pady=2)

        # Action buttons
        ctk.CTkFrame(left, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=6)
        ctk.CTkButton(left, text="▶  RUN SIMULATION",
                      fg_color=ACCENT, text_color=BG, hover_color="#00b894",
                      font=ctk.CTkFont("Consolas", 13, "bold"), height=40,
                      command=self._run).pack(fill="x", padx=16, pady=4)

        b1 = ctk.CTkFrame(left, fg_color=PANEL)
        b1.pack(fill="x", padx=16, pady=2)
        for text, cmd in [("✕ Clear", self._clear),
                          ("💾 CSV", self._export),
                          ("📄 PDF", self._export_pdf)]:
            ctk.CTkButton(b1, text=text, fg_color=CARD, hover_color=BORDER,
                          text_color=SUBTEXT, font=ctk.CTkFont("Consolas", 10),
                          command=cmd).pack(side="left", expand=True, fill="x", padx=1)

        b2 = ctk.CTkFrame(left, fg_color=PANEL)
        b2.pack(fill="x", padx=16, pady=2)
        for text, cmd in [("📂 Load Config", self._load_config),
                          ("💿 Save Config", self._save_config)]:
            ctk.CTkButton(b2, text=text, fg_color=CARD, hover_color=BORDER,
                          text_color=SUBTEXT, font=ctk.CTkFont("Consolas", 10),
                          command=cmd).pack(side="left", expand=True, fill="x", padx=1)

        # Preset scenarios
        ctk.CTkFrame(left, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=6)
        ctk.CTkLabel(left, text="PRESETS",
                     font=ctk.CTkFont("Consolas", 10, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(0, 4))
        pg = ctk.CTkFrame(left, fg_color=PANEL)
        pg.pack(fill="x", padx=16, pady=2)
        for i, name in enumerate(PRESETS):
            r, c = divmod(i, 2)
            ctk.CTkButton(
                pg, text=name, fg_color=ACCENT2, hover_color="#6d28d9",
                text_color=TEXT, font=ctk.CTkFont("Consolas", 9),
                command=lambda n=name: self._load_preset(n),
            ).grid(row=r, column=c, padx=2, pady=2, sticky="ew")
        pg.columnconfigure(0, weight=1)
        pg.columnconfigure(1, weight=1)

    # ── Right panel ────────────────────────────────────────────────────────────
    def _build_right(self, main):
        right = ctk.CTkFrame(main, fg_color=BG)
        right.pack(side="right", fill="both", expand=True)

        # Stats cards row
        self.stats_frame = ctk.CTkFrame(right, fg_color=BG)
        self.stats_frame.pack(fill="x", padx=16, pady=(10, 0))

        # Analysis label
        self.analysis_label = ctk.CTkLabel(
            right, text="", font=ctk.CTkFont("Consolas", 11),
            text_color="#4ade80", wraplength=760, justify="left")
        self.analysis_label.pack(fill="x", padx=16, pady=(2, 0))

        # ── Gantt header row (title + animation controls) ──
        gh = ctk.CTkFrame(right, fg_color=BG)
        gh.pack(fill="x", padx=16, pady=(8, 2))
        ctk.CTkLabel(gh, text="GANTT CHART",
                     font=ctk.CTkFont("Consolas", 10, "bold"),
                     text_color=ACCENT).pack(side="left")

        ac = ctk.CTkFrame(gh, fg_color=BG)
        ac.pack(side="right")
        ctk.CTkButton(ac, text="◀", width=28, fg_color=CARD, hover_color=BORDER,
                      text_color=TEXT, font=ctk.CTkFont("Consolas", 12),
                      command=self._step_back).pack(side="left", padx=1)
        ctk.CTkButton(ac, text="▶ Animate", width=88, fg_color=ACCENT2,
                      hover_color="#6d28d9", text_color=TEXT,
                      font=ctk.CTkFont("Consolas", 10),
                      command=self._animate).pack(side="left", padx=1)
        ctk.CTkButton(ac, text="▶", width=28, fg_color=CARD, hover_color=BORDER,
                      text_color=TEXT, font=ctk.CTkFont("Consolas", 12),
                      command=self._step_fwd).pack(side="left", padx=1)
        ctk.CTkButton(ac, text="⏹ Reset", width=68, fg_color=CARD, hover_color=BORDER,
                      text_color=SUBTEXT, font=ctk.CTkFont("Consolas", 10),
                      command=self._anim_reset).pack(side="left", padx=1)
        ctk.CTkLabel(ac, text="Speed:", font=ctk.CTkFont("Consolas", 9),
                     text_color=SUBTEXT).pack(side="left", padx=(8, 2))
        self.speed_slider = ctk.CTkSlider(ac, from_=1, to=10, width=80,
                                          fg_color=CARD, progress_color=ACCENT,
                                          button_color=ACCENT)
        self.speed_slider.set(5)
        self.speed_slider.pack(side="left")

        # Gantt canvas
        self.gantt_canvas = Canvas(right, bg=CARD, height=88,
                                   highlightthickness=0, bd=0)
        self.gantt_canvas.pack(fill="x", padx=16, pady=(0, 4))

        # State timeline
        ctk.CTkLabel(
            right,
            text="PROCESS STATE TIMELINE   ■ Ready  ■ Running  ■ Done",
            font=ctk.CTkFont("Consolas", 9, "bold"),
            text_color=ACCENT,
        ).pack(anchor="w", padx=16, pady=(4, 2))
        self.state_canvas = Canvas(right, bg=CARD, height=60,
                                   highlightthickness=0, bd=0)
        self.state_canvas.pack(fill="x", padx=16, pady=(0, 4))

        # RR quantum chart (hidden until RR selected)
        self.rr_lbl = ctk.CTkLabel(right, text="ROUND ROBIN — Avg WT vs Time Quantum",
                                   font=ctk.CTkFont("Consolas", 9, "bold"),
                                   text_color=ACCENT)
        self.rr_canvas = Canvas(right, bg=CARD, height=90,
                                highlightthickness=0, bd=0)

        # Results table
        ctk.CTkLabel(right, text="RESULTS TABLE",
                     font=ctk.CTkFont("Consolas", 10, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(6, 2))
        self.table_frame = ctk.CTkScrollableFrame(right, fg_color=CARD, height=170)
        self.table_frame.pack(fill="both", expand=True, padx=16, pady=(0, 8))

    # ════════════════════════════════════════════════════════════════════════════
    # EVENT HANDLERS
    # ════════════════════════════════════════════════════════════════════════════

    def _on_algo_change(self):
        algo = self.algo_var.get()
        if algo in ("rr", "mlfq"):
            self.q_frame.pack(fill="x", padx=20, pady=4)
        else:
            self.q_frame.pack_forget()
        if algo == "pri":
            self.aging_frame.pack(fill="x", padx=20, pady=2)
        else:
            self.aging_frame.pack_forget()
        if algo == "rr":
            self.rr_lbl.pack(anchor="w", padx=16, pady=(4, 2))
            self.rr_canvas.pack(fill="x", padx=16, pady=(0, 4))
        else:
            self.rr_lbl.pack_forget()
            self.rr_canvas.pack_forget()

    def _gen(self):
        for w in self.proc_scroll.winfo_children():
            w.destroy()
        self.rows.clear()
        try:
            n = int(self.n_entry.get())
            assert 1 <= n <= 15
        except Exception:
            messagebox.showerror("Error", "Enter 1–15")
            return
        for i in range(n):
            self._add_row(i, str(i), str(random.randint(1, 8)), str(random.randint(1, 3)))

    def _random(self):
        try:
            n = int(self.n_entry.get())
        except Exception:
            n = 5
        procs = generate_random_processes(n)
        for w in self.proc_scroll.winfo_children():
            w.destroy()
        self.rows.clear()
        for pid, at, bt, pri in procs:
            self._add_row(pid - 1, str(at), str(bt), str(pri))

    def _add_row(self, i, at, bt, pri):
        color = COLORS[i % len(COLORS)]
        row = ctk.CTkFrame(self.proc_scroll, fg_color=PANEL)
        row.pack(fill="x", pady=1)
        ctk.CTkLabel(row, text=f"P{i+1}",
                     font=ctk.CTkFont("Consolas", 9, "bold"),
                     text_color=BG, fg_color=color,
                     width=35, corner_radius=4).pack(side="left", padx=2)
        e_at  = ctk.CTkEntry(row, width=44, font=ctk.CTkFont("Consolas", 10))
        e_at.insert(0, at);  e_at.pack(side="left", padx=2)
        e_bt  = ctk.CTkEntry(row, width=44, font=ctk.CTkFont("Consolas", 10))
        e_bt.insert(0, bt);  e_bt.pack(side="left", padx=2)
        e_pri = ctk.CTkEntry(row, width=38, font=ctk.CTkFont("Consolas", 10))
        e_pri.insert(0, pri); e_pri.pack(side="left", padx=2)
        self.rows.append({"at": e_at, "bt": e_bt, "pri": e_pri, "color": color})

    def _run(self):
        if not self.rows:
            messagebox.showwarning("No Data", "Generate processes first.")
            return
        algo = self.algo_var.get()
        processes = []
        for i, r in enumerate(self.rows):
            try:
                at = int(r["at"].get()); bt = int(r["bt"].get()); pri = int(r["pri"].get())
                assert at >= 0 and bt > 0
                processes.append((i + 1, at, bt, pri))
            except Exception:
                messagebox.showerror("Error", f"Invalid input for P{i+1}")
                return

        try:
            q = int(self.q_entry.get()) if algo in ("rr", "mlfq") else 2
        except Exception:
            q = 2

        self._aging_log = []
        if algo == "pri" and self.aging_var.get():
            result, gantt, self._aging_log = priority_scheduling_aging(processes)
        else:
            funcs = {
                "fcfs": lambda: fcfs(processes),
                "sjf":  lambda: sjf(processes),
                "srtf": lambda: srtf(processes),
                "rr":   lambda: round_robin(processes, q),
                "pri":  lambda: priority_scheduling(processes),
                "mlq":  lambda: multilevel_queue(processes, q),
                "mlfq": lambda: mlfq(processes, max(1, q // 2), q),
            }
            result, gantt = funcs[algo]()

        self._last_procs  = processes
        self.last_result  = result
        self.gantt_data   = gantt
        self._anim_step   = len(gantt)  # full chart shown immediately

        self._draw_gantt_steps(len(gantt))
        self._draw_state_timeline(processes, gantt, result)
        self._draw_table(result, processes, gantt)
        self._draw_stats(result, gantt)

        if algo == "rr":
            self._draw_rr_chart(processes)

    # ════════════════════════════════════════════════════════════════════════════
    # GANTT — ANIMATION
    # ════════════════════════════════════════════════════════════════════════════

    def _draw_gantt_steps(self, n_steps):
        """Render the first n_steps blocks of the stored Gantt chart."""
        c = self.gantt_canvas
        c.delete("all")
        if not self.gantt_data:
            return
        c.update_idletasks()
        W    = max(c.winfo_width(), 600)
        pad  = 10;  bar_h = 44
        y0, y1 = 14, 14 + bar_h
        total  = max(g[2] for g in self.gantt_data)
        scale  = (W - 2 * pad) / max(total, 1)
        pid_col = {i + 1: r["color"] for i, r in enumerate(self.rows)}
        visible = self.gantt_data[:n_steps]

        for idx, (pid, start, end) in enumerate(visible):
            x0  = pad + start * scale
            x1  = pad + end   * scale
            col = pid_col.get(pid, ACCENT)
            if idx == n_steps - 1 and n_steps < len(self.gantt_data):
                # Highlight the "currently arriving" block
                c.create_rectangle(x0 - 2, y0 - 2, x1 + 2, y1 + 2,
                                   fill="#ffffff", outline="")
            c.create_rectangle(x0, y0, x1, y1, fill=col, outline="")
            if x1 - x0 > 18:
                c.create_text((x0 + x1) / 2, (y0 + y1) / 2,
                              text=f"P{pid}",
                              font=("Consolas", 8, "bold"), fill=BG)
            c.create_line(x0, y1, x0, y1 + 5, fill=SUBTEXT)
            c.create_text(x0, y1 + 13, text=str(start),
                          font=("Consolas", 7), fill=SUBTEXT)

        if visible:
            x_end = pad + visible[-1][2] * scale
            c.create_line(x_end, y1, x_end, y1 + 5, fill=SUBTEXT)
            c.create_text(x_end, y1 + 13, text=str(visible[-1][2]),
                          font=("Consolas", 7), fill=SUBTEXT)

    def _animate(self):
        """Start the step-by-step Gantt animation from the beginning."""
        if not self.gantt_data:
            return
        if self._anim_id:
            self.gantt_canvas.after_cancel(self._anim_id)
            self._anim_id = None
        self._anim_step = 0
        self._anim_tick()

    def _anim_tick(self):
        if self._anim_step >= len(self.gantt_data):
            return
        self._anim_step += 1
        self._draw_gantt_steps(self._anim_step)
        delay = int(1100 - self.speed_slider.get() * 100)   # speed=1 → 1000 ms, speed=10 → 100 ms
        self._anim_id = self.gantt_canvas.after(delay, self._anim_tick)

    def _step_fwd(self):
        if not self.gantt_data:
            return
        if self._anim_id:
            self.gantt_canvas.after_cancel(self._anim_id)
            self._anim_id = None
        self._anim_step = min(self._anim_step + 1, len(self.gantt_data))
        self._draw_gantt_steps(self._anim_step)

    def _step_back(self):
        if not self.gantt_data:
            return
        if self._anim_id:
            self.gantt_canvas.after_cancel(self._anim_id)
            self._anim_id = None
        self._anim_step = max(self._anim_step - 1, 0)
        self._draw_gantt_steps(self._anim_step)

    def _anim_reset(self):
        if self._anim_id:
            self.gantt_canvas.after_cancel(self._anim_id)
            self._anim_id = None
        self._anim_step = 0
        self.gantt_canvas.delete("all")

    # ════════════════════════════════════════════════════════════════════════════
    # PROCESS STATE TIMELINE
    # ════════════════════════════════════════════════════════════════════════════

    def _draw_state_timeline(self, processes, gantt, result):
        """
        Horizontal grid: each row = one process, each cell = one time unit.
        Yellow = Ready (arrived, waiting),  Green = Running,  Grey = Done.

        State colours are determined in a single forward pass (O(n + m) where
        n = number of processes and m = total time), then rendered per process.
        """
        c = self.state_canvas
        c.delete("all")
        if not gantt or not processes:
            return
        c.update_idletasks()
        W = max(c.winfo_width(), 600)
        H = 60
        n = len(processes)

        total_time = max(g[2] for g in gantt)
        if total_time == 0:
            return
        pad_x = 36
        scale  = (W - pad_x - 4) / total_time
        row_h  = max(4, min(16, (H - 4) / n))

        # Build running_map and finish_map in a single pass each
        running_map: dict[int, int] = {}   # time → pid
        for pid, start, end in gantt:
            for t in range(start, end):
                running_map[t] = pid

        finish_map: dict[int, int] = {}    # pid → finish time
        for r in result:
            finish_map[r[0]] = r[1] + r[4]   # arrival + tat

        # Build state grid: state_grid[i][t] = fill colour (one pass per process)
        pid_arrival = {p[0]: p[1] for p in processes}
        for i, (pid, arrival, burst, pri) in enumerate(processes):
            y = 2 + i * row_h
            col = COLORS[i % len(COLORS)]
            c.create_text(pad_x - 3, y + row_h / 2,
                          text=f"P{pid}", font=("Consolas", 7, "bold"),
                          fill=col, anchor="e")
            finish = finish_map.get(pid, total_time)
            for t in range(total_time):
                if t < arrival:
                    fill = BG
                elif running_map.get(t) == pid:
                    fill = "#4ade80"   # running — green
                elif finish <= t:
                    fill = "#8b949e"   # done — grey
                else:
                    fill = "#f59e0b"   # ready — amber
                x0 = pad_x + t * scale
                x1 = pad_x + (t + 1) * scale
                # min-width of 1px ensures visibility at very fine time scales
                c.create_rectangle(x0, y, max(x0 + 1, x1),
                                   y + row_h - 1, fill=fill, outline="")

        # Legend
        for j, (label, col) in enumerate([("Ready", "#f59e0b"),
                                           ("Running", "#4ade80"),
                                           ("Done", "#8b949e")]):
            c.create_rectangle(W - 120 + j * 40, 2, W - 108 + j * 40, 10,
                               fill=col, outline="")
            c.create_text(W - 106 + j * 40, 6, text=label,
                          font=("Consolas", 6), fill=TEXT, anchor="w")

    # ════════════════════════════════════════════════════════════════════════════
    # RESULTS TABLE
    # ════════════════════════════════════════════════════════════════════════════

    def _draw_table(self, result, processes, gantt):
        for w in self.table_frame.winfo_children():
            w.destroy()
        rt_map = response_times(processes, gantt)
        hdr = ctk.CTkFrame(self.table_frame, fg_color=PANEL)
        hdr.pack(fill="x", pady=(0, 4))
        cols = ["PID", "Arrival", "Burst", "Waiting", "Turnaround", "Response", "Resp Ratio"]
        for col in cols:
            ctk.CTkLabel(hdr, text=col,
                         font=ctk.CTkFont("Consolas", 10, "bold"),
                         text_color=ACCENT, width=90).pack(side="left", padx=2)
        for r in result:
            pid, at, bt, wt, tat = r
            rt  = rt_map.get(pid, 0)
            rr  = f"{tat / bt:.2f}" if bt else "–"
            row = ctk.CTkFrame(self.table_frame, fg_color=CARD)
            row.pack(fill="x", pady=1)
            col = COLORS[(pid - 1) % len(COLORS)]
            for val in [f"P{pid}", at, bt, wt, tat, rt, rr]:
                ctk.CTkLabel(row, text=str(val),
                             font=ctk.CTkFont("Consolas", 10),
                             text_color=col, width=90).pack(side="left", padx=2)

    # ════════════════════════════════════════════════════════════════════════════
    # STATS CARDS
    # ════════════════════════════════════════════════════════════════════════════

    def _draw_stats(self, result, gantt):
        for w in self.stats_frame.winfo_children():
            w.destroy()
        wts  = [r[3] for r in result]
        tats = [r[4] for r in result]
        avg_wt  = sum(wts) / len(wts)
        avg_tat = sum(tats) / len(tats)
        total_burst = sum(r[2] for r in result)
        makespan    = max(r[1] + r[4] for r in result)
        cpu_util    = total_burst / makespan * 100 if makespan else 0
        ctx_sw      = context_switches(gantt)
        throughput  = round(len(result) / makespan, 3) if makespan else 0

        cards = [
            ("Avg WT",     f"{avg_wt:.2f}",    "#f59e0b"),
            ("Avg TAT",    f"{avg_tat:.2f}",   "#60a5fa"),
            ("CPU Util",   f"{cpu_util:.1f}%", "#4ade80"),
            ("Ctx Sw",     str(ctx_sw),         "#f87171"),
            ("Throughput", str(throughput),     ACCENT),
        ]
        for label, val, col in cards:
            card = ctk.CTkFrame(self.stats_frame, fg_color=CARD, corner_radius=8)
            card.pack(side="left", padx=(0, 6), pady=4)
            ctk.CTkLabel(card, text=val,
                         font=ctk.CTkFont("Consolas", 18, "bold"),
                         text_color=col).pack(padx=10, pady=(6, 0))
            ctk.CTkLabel(card, text=label,
                         font=ctk.CTkFont("Consolas", 9),
                         text_color=SUBTEXT).pack(padx=10, pady=(0, 6))

        best_p  = min(result, key=lambda r: r[3])
        worst_p = max(result, key=lambda r: r[3])
        aging_note = (f"  |  ⏫ Aging applied {len(self._aging_log)}× — starvation prevented"
                      if self._aging_log else "")
        self.analysis_label.configure(
            text=(f"📊 Avg WT={avg_wt:.2f} | Avg TAT={avg_tat:.2f} | "
                  f"Context Switches={ctx_sw} | Throughput={throughput} proc/unit | "
                  f"Best: P{best_p[0]} (WT={best_p[3]}) | Worst: P{worst_p[0]} (WT={worst_p[3]})"
                  f"{aging_note}"))

    # ════════════════════════════════════════════════════════════════════════════
    # RR QUANTUM ANALYSIS CHART
    # ════════════════════════════════════════════════════════════════════════════

    def _draw_rr_chart(self, processes):
        """Bar chart: x = quantum (1–10), y = average waiting time."""
        data = throughput_vs_quantum(processes)
        c = self.rr_canvas
        c.delete("all")
        c.update_idletasks()
        W = max(c.winfo_width(), 600)
        H = 88
        if not data:
            return
        pad_x, pad_y = 36, 8
        max_wt = max(d[1] for d in data) or 1
        bar_w  = (W - 2 * pad_x) / len(data)

        for i, (q, avg_wt, avg_tat) in enumerate(data):
            x0 = pad_x + i * bar_w + bar_w * 0.1
            x1 = pad_x + i * bar_w + bar_w * 0.9
            bh = (avg_wt / max_wt) * (H - 2 * pad_y - 18)
            y0 = H - pad_y - 18 - bh
            y1 = H - pad_y - 18
            c.create_rectangle(x0, y0, x1, y1, fill="#60a5fa", outline="")
            c.create_text((x0 + x1) / 2, y0 - 6,
                          text=f"{avg_wt:.1f}", font=("Consolas", 7), fill=TEXT)
            c.create_text((x0 + x1) / 2, H - 8,
                          text=f"q={q}", font=("Consolas", 7), fill=SUBTEXT)
        c.create_text(pad_x - 2, H // 2,
                      text="WT", font=("Consolas", 7), fill=SUBTEXT, angle=90)

    # ════════════════════════════════════════════════════════════════════════════
    # SAVE / LOAD CONFIG
    # ════════════════════════════════════════════════════════════════════════════

    def _save_config(self):
        if not self.rows:
            messagebox.showinfo("No Data", "Generate processes first.")
            return
        processes = []
        for i, r in enumerate(self.rows):
            try:
                processes.append({
                    "pid": i + 1,
                    "at":  int(r["at"].get()),
                    "bt":  int(r["bt"].get()),
                    "pri": int(r["pri"].get()),
                })
            except Exception:
                messagebox.showerror("Error", f"Invalid input for P{i+1}")
                return
        config = {
            "algorithm": self.algo_var.get(),
            "quantum":   self.q_entry.get(),
            "processes": processes,
        }
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Process Configuration",
        )
        if not path:
            return
        with open(path, "w") as f:
            json.dump(config, f, indent=2)
        messagebox.showinfo("Saved", f"Config saved to:\n{path}")

    def _load_config(self):
        path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json")],
            title="Load Process Configuration",
        )
        if not path:
            return
        try:
            with open(path) as f:
                config = json.load(f)
            self.algo_var.set(config.get("algorithm", "fcfs"))
            self.q_entry.delete(0, "end")
            self.q_entry.insert(0, config.get("quantum", "2"))
            self._on_algo_change()
            for w in self.proc_scroll.winfo_children():
                w.destroy()
            self.rows.clear()
            for p in config["processes"]:
                self._add_row(p["pid"] - 1, str(p["at"]), str(p["bt"]), str(p["pri"]))
            self.n_entry.delete(0, "end")
            self.n_entry.insert(0, str(len(config["processes"])))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config:\n{e}")

    def _load_preset(self, name):
        procs = PRESETS.get(name, [])
        for w in self.proc_scroll.winfo_children():
            w.destroy()
        self.rows.clear()
        for pid, at, bt, pri in procs:
            self._add_row(pid - 1, str(at), str(bt), str(pri))
        self.n_entry.delete(0, "end")
        self.n_entry.insert(0, str(len(procs)))

    # ════════════════════════════════════════════════════════════════════════════
    # CLEAR / EXPORT
    # ════════════════════════════════════════════════════════════════════════════

    def _clear(self):
        if self._anim_id:
            self.gantt_canvas.after_cancel(self._anim_id)
            self._anim_id = None
        for w in self.proc_scroll.winfo_children():
            w.destroy()
        self.rows.clear()
        self.gantt_canvas.delete("all")
        self.state_canvas.delete("all")
        self.rr_canvas.delete("all")
        for w in self.table_frame.winfo_children():
            w.destroy()
        for w in self.stats_frame.winfo_children():
            w.destroy()
        self.analysis_label.configure(text="")
        self.last_result = None
        self.gantt_data  = []
        self._anim_step  = 0

    def _export(self):
        if not self.last_result:
            messagebox.showinfo("No Data", "Run a simulation first.")
            return
        path = os.path.join(os.path.dirname(__file__), "..", "output", "cpu_results.csv")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["PID", "Arrival", "Burst", "Waiting", "Turnaround"])
            for r in self.last_result:
                w.writerow([f"P{r[0]}", r[1], r[2], r[3], r[4]])
        messagebox.showinfo("Exported", f"CSV saved to:\n{os.path.abspath(path)}")

    def _export_pdf(self):
        if not self.last_result:
            messagebox.showinfo("No Data", "Run a simulation first.")
            return
        try:
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
            from generate_report import generate_simulation_report
        except ImportError:
            messagebox.showerror("Missing Library",
                                 "fpdf2 is required.\n\nInstall with:  pip install fpdf2")
            return

        wts  = [r[3] for r in self.last_result]
        tats = [r[4] for r in self.last_result]
        avg_wt  = sum(wts) / len(wts)
        avg_tat = sum(tats) / len(tats)
        total_burst = sum(r[2] for r in self.last_result)
        makespan    = max(r[1] + r[4] for r in self.last_result)
        stats = {
            "algo":             self.algo_var.get().upper(),
            "avg_wt":           avg_wt,
            "avg_tat":          avg_tat,
            "context_switches": context_switches(self.gantt_data),
            "cpu_util":         total_burst / makespan * 100 if makespan else 0,
            "throughput":       round(len(self.last_result) / makespan, 3) if makespan else 0,
        }
        path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            title="Save Simulation Report",
        )
        if not path:
            return
        try:
            generate_simulation_report(
                self.last_result, self._last_procs, self.gantt_data, stats, path
            )
            messagebox.showinfo("Exported", f"PDF saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
