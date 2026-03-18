import tkinter as tk
from tkinter import ttk, messagebox
import math

# ── Palette ────────────────────────────────────────────────────────────────────
BG        = "#0d1117"
PANEL     = "#161b22"
CARD      = "#1c2230"
BORDER    = "#30363d"
ACCENT    = "#00d4aa"
ACCENT2   = "#7c3aed"
WARN      = "#f59e0b"
TEXT      = "#e6edf3"
SUBTEXT   = "#8b949e"
RED       = "#f87171"
GREEN     = "#4ade80"
BLUE      = "#60a5fa"
PINK      = "#f472b6"

PROCESS_COLORS = [ACCENT, ACCENT2, WARN, RED, GREEN, BLUE, PINK,
                  "#fb923c", "#34d399", "#a78bfa"]

FONT_TITLE  = ("Courier New", 22, "bold")
FONT_HEAD   = ("Courier New", 11, "bold")
FONT_BODY   = ("Courier New", 10)
FONT_SMALL  = ("Courier New", 9)
FONT_MONO   = ("Courier New", 10)

# ── Scheduling algorithms ──────────────────────────────────────────────────────

def fcfs(processes):
    procs = sorted(processes, key=lambda x: (x[1], x[0]))
    time, result = 0, []
    for pid, arrival, burst, _ in procs:
        if time < arrival:
            time = arrival
        wt = time - arrival
        time += burst
        result.append((pid, arrival, burst, wt, wt + burst))
    return result


def sjf_non_preemptive(processes):
    procs = [list(p) for p in processes]
    time, done, result = 0, [], []
    remaining = procs[:]
    while remaining:
        available = [p for p in remaining if p[1] <= time]
        if not available:
            time = min(p[1] for p in remaining)
            available = [p for p in remaining if p[1] <= time]
        chosen = min(available, key=lambda x: x[2])
        remaining.remove(chosen)
        pid, arrival, burst = chosen[0], chosen[1], chosen[2]
        if time < arrival:
            time = arrival
        wt = time - arrival
        time += burst
        result.append((pid, arrival, burst, wt, wt + burst))
    return result


def round_robin(processes, quantum):
    from collections import deque
    procs = sorted(processes, key=lambda x: x[1])
    n = len(procs)
    remaining  = [p[2] for p in procs]
    finish     = [0] * n
    arrival    = [p[1] for p in procs]
    burst      = [p[2] for p in procs]
    pids       = [p[0] for p in procs]

    queue = deque()
    time = 0
    visited = [False] * n
    i = 0

    # seed first arrivals
    while i < n and arrival[i] <= time:
        queue.append(i)
        visited[i] = True
        i += 1

    gantt = []
    while queue:
        idx = queue.popleft()
        run = min(quantum, remaining[idx])
        gantt.append((pids[idx], time, time + run))
        time += run
        remaining[idx] -= run

        # enqueue newly arrived
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


def priority_non_preemptive(processes):
    procs = [list(p) for p in processes]
    time, result = 0, []
    remaining = procs[:]
    while remaining:
        available = [p for p in remaining if p[1] <= time]
        if not available:
            time = min(p[1] for p in remaining)
            available = [p for p in remaining if p[1] <= time]
        chosen = min(available, key=lambda x: x[3])
        remaining.remove(chosen)
        pid, arrival, burst, pri = chosen
        if time < arrival:
            time = arrival
        wt = time - arrival
        time += burst
        result.append((pid, arrival, burst, wt, wt + burst))
    return result


def build_gantt_from_result(result):
    """Build a simple (sequential) Gantt from FCFS/SJF/Priority result."""
    gantt = []
    time = 0
    for pid, arrival, burst, wt, tat in result:
        start = arrival + wt
        gantt.append((pid, start, start + burst))
    return gantt


# ── Main Application ───────────────────────────────────────────────────────────

class CPUSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1080x780")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.process_rows = []
        self.result_data  = []
        self.gantt_data   = []

        self._build_ui()

    # ── UI construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Header bar ──
        header = tk.Frame(self.root, bg=PANEL, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="⚙  CPU SCHEDULING SIMULATOR",
                 font=FONT_TITLE, bg=PANEL, fg=ACCENT).pack(side="left", padx=24, pady=12)

        tk.Label(header, text="by Process Planner v2.0",
                 font=FONT_SMALL, bg=PANEL, fg=SUBTEXT).pack(side="right", padx=24, pady=18)

        # thin accent line
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill="x")

        # ── Body: left panel + right panel ──
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=0, pady=0)

        left  = self._left_panel(body)
        right = self._right_panel(body)
        left.pack (side="left",  fill="y",    padx=0, pady=0)
        right.pack(side="right", fill="both", expand=True, padx=0, pady=0)

    # ─── Left control panel ───────────────────────────────────────────────────

    def _left_panel(self, parent):
        frame = tk.Frame(parent, bg=PANEL, width=320)
        frame.pack_propagate(False)

        self._section(frame, "ALGORITHM")

        self.algo_var = tk.StringVar(value="FCFS")
        algos = [("FCFS",            "fcfs"),
                 ("SJF (Non-Preemptive)", "sjf"),
                 ("Round Robin",     "rr"),
                 ("Priority (Non-Preemptive)", "pri")]

        for label, val in algos:
            rb = tk.Radiobutton(frame, text=label, variable=self.algo_var,
                                value=val, font=FONT_BODY, bg=PANEL, fg=TEXT,
                                selectcolor=CARD, activebackground=PANEL,
                                activeforeground=ACCENT, indicatoron=0,
                                relief="flat", padx=12, pady=6,
                                cursor="hand2",
                                command=self._on_algo_change)
            rb.pack(fill="x", padx=16, pady=2)

        # quantum row (hidden unless RR)
        self.quantum_frame = tk.Frame(frame, bg=PANEL)
        self.quantum_frame.pack(fill="x", padx=16, pady=(0, 4))
        tk.Label(self.quantum_frame, text="Time Quantum:", font=FONT_BODY,
                 bg=PANEL, fg=SUBTEXT).pack(side="left")
        self.quantum_entry = self._entry(self.quantum_frame, width=5)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.pack(side="left", padx=8)
        self.quantum_frame.pack_forget()

        self._divider(frame)
        self._section(frame, "PROCESSES")

        ctrl = tk.Frame(frame, bg=PANEL)
        ctrl.pack(fill="x", padx=16, pady=4)
        tk.Label(ctrl, text="Count:", font=FONT_BODY, bg=PANEL, fg=SUBTEXT).pack(side="left")
        self.num_entry = self._entry(ctrl, width=4)
        self.num_entry.insert(0, "4")
        self.num_entry.pack(side="left", padx=8)
        self._btn(ctrl, "Generate", self._create_inputs, ACCENT2).pack(side="left")

        # table header
        hdr = tk.Frame(frame, bg=CARD)
        hdr.pack(fill="x", padx=16, pady=(8, 0))
        for col, w in [("PID", 4), ("Arrival", 7), ("Burst", 6), ("Priority", 8)]:
            tk.Label(hdr, text=col, font=FONT_SMALL, bg=CARD, fg=SUBTEXT,
                     width=w, anchor="center").pack(side="left", padx=2, pady=4)

        self.process_frame = tk.Frame(frame, bg=PANEL)
        self.process_frame.pack(fill="x", padx=16)

        self._divider(frame)

        run_btn = tk.Button(frame, text="▶  RUN SIMULATION",
                            font=("Courier New", 12, "bold"),
                            bg=ACCENT, fg=BG, relief="flat",
                            activebackground="#00b894", activeforeground=BG,
                            cursor="hand2", pady=10,
                            command=self._run_simulation)
        run_btn.pack(fill="x", padx=16, pady=8)

        clr_btn = tk.Button(frame, text="✕  Clear All",
                            font=FONT_SMALL, bg=CARD, fg=SUBTEXT,
                            relief="flat", activebackground=BORDER,
                            activeforeground=TEXT, cursor="hand2", pady=6,
                            command=self._clear_all)
        clr_btn.pack(fill="x", padx=16, pady=(0, 8))

        return frame

    # ─── Right results panel ──────────────────────────────────────────────────

    def _right_panel(self, parent):
        frame = tk.Frame(parent, bg=BG)

        # Stats row
        self.stats_frame = tk.Frame(frame, bg=BG)
        self.stats_frame.pack(fill="x", padx=16, pady=(12, 0))

        # Gantt chart canvas
        self._section_label(frame, "GANTT CHART")
        self.gantt_canvas = tk.Canvas(frame, bg=CARD, height=100,
                                      highlightthickness=0)
        self.gantt_canvas.pack(fill="x", padx=16, pady=(4, 0))

        # Results table
        self._section_label(frame, "RESULTS TABLE")
        tbl_frame = tk.Frame(frame, bg=CARD)
        tbl_frame.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=CARD, foreground=TEXT,
                        fieldbackground=CARD, borderwidth=0,
                        font=FONT_MONO, rowheight=28)
        style.configure("Custom.Treeview.Heading",
                        background=PANEL, foreground=ACCENT,
                        font=FONT_HEAD, relief="flat")
        style.map("Custom.Treeview",
                  background=[("selected", ACCENT2)],
                  foreground=[("selected", TEXT)])

        cols = ("PID", "Arrival Time", "Burst Time", "Waiting Time",
                "Turnaround Time", "Response Ratio")
        self.tree = ttk.Treeview(tbl_frame, columns=cols, show="headings",
                                  style="Custom.Treeview")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center",
                             width=140 if "Time" in col or "Ratio" in col else 60)

        vsb = ttk.Scrollbar(tbl_frame, orient="vertical",   command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        return frame

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _section(self, parent, text):
        f = tk.Frame(parent, bg=PANEL)
        f.pack(fill="x", padx=16, pady=(12, 4))
        tk.Label(f, text=text, font=("Courier New", 9, "bold"),
                 bg=PANEL, fg=ACCENT).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(8, 0), pady=6)

    def _section_label(self, parent, text):
        f = tk.Frame(parent, bg=BG)
        f.pack(fill="x", padx=16, pady=(10, 2))
        tk.Label(f, text=text, font=("Courier New", 9, "bold"),
                 bg=BG, fg=ACCENT).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=(8, 0), pady=6)

    def _divider(self, parent):
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=16, pady=8)

    def _entry(self, parent, width=8):
        e = tk.Entry(parent, width=width, bg=CARD, fg=TEXT,
                     insertbackground=ACCENT, relief="flat",
                     font=FONT_BODY, highlightthickness=1,
                     highlightcolor=ACCENT, highlightbackground=BORDER)
        return e

    def _btn(self, parent, text, cmd, color=ACCENT):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg=BG, font=FONT_SMALL,
                         relief="flat", padx=8, pady=4,
                         activebackground=ACCENT2, activeforeground=TEXT,
                         cursor="hand2")

    # ── Process row management ─────────────────────────────────────────────────

    def _on_algo_change(self):
        if self.algo_var.get() == "rr":
            self.quantum_frame.pack(fill="x", padx=16, pady=(0, 4))
        else:
            self.quantum_frame.pack_forget()
        # show/hide priority column header hint
        self._refresh_column_visibility()

    def _refresh_column_visibility(self):
        show_pri = self.algo_var.get() == "pri"
        for row_data in self.process_rows:
            if show_pri:
                row_data["pri_entry"].grid()
            else:
                row_data["pri_entry"].grid_remove()

    def _create_inputs(self):
        for widget in self.process_frame.winfo_children():
            widget.destroy()
        self.process_rows.clear()

        try:
            n = int(self.num_entry.get())
            if not 1 <= n <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Enter a number between 1 and 10.")
            return

        show_pri = self.algo_var.get() == "pri"

        for i in range(n):
            color = PROCESS_COLORS[i % len(PROCESS_COLORS)]
            row_f = tk.Frame(self.process_frame, bg=PANEL)
            row_f.pack(fill="x", pady=2)

            # colour badge
            badge = tk.Label(row_f, text=f"P{i+1}", font=("Courier New", 9, "bold"),
                             bg=color, fg=BG, width=4)
            badge.pack(side="left", padx=(0, 4))

            arr = self._entry(row_f, width=6)
            arr.pack(side="left", padx=2)
            arr.insert(0, str(i))          # sensible default

            bst = self._entry(row_f, width=5)
            bst.pack(side="left", padx=2)
            bst.insert(0, str(4 - i % 4 + 1))

            pri_e = self._entry(row_f, width=5)
            pri_e.pack(side="left", padx=2)
            pri_e.insert(0, str(i + 1))
            if not show_pri:
                pri_e.pack_forget()

            self.process_rows.append({
                "arrival": arr,
                "burst":   bst,
                "pri_entry": pri_e,
                "color":   color,
            })

    def _clear_all(self):
        for widget in self.process_frame.winfo_children():
            widget.destroy()
        self.process_rows.clear()
        self.gantt_canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        for w in self.stats_frame.winfo_children():
            w.destroy()

    # ── Simulation ─────────────────────────────────────────────────────────────

    def _run_simulation(self):
        if not self.process_rows:
            messagebox.showwarning("No Processes", "Generate a process table first.")
            return

        algo = self.algo_var.get()
        processes = []
        for i, row in enumerate(self.process_rows):
            try:
                arr  = int(row["arrival"].get())
                bst  = int(row["burst"].get())
                pri  = int(row["pri_entry"].get()) if algo == "pri" else 0
                if arr < 0 or bst <= 0:
                    raise ValueError
                processes.append((i + 1, arr, bst, pri))
            except ValueError:
                messagebox.showerror("Input Error",
                    f"Invalid values for P{i+1}. Arrival ≥ 0, Burst > 0.")
                return

        gantt = None
        if algo == "fcfs":
            result = fcfs(processes)
            gantt  = build_gantt_from_result(result)
        elif algo == "sjf":
            result = sjf_non_preemptive(processes)
            gantt  = build_gantt_from_result(result)
        elif algo == "rr":
            try:
                q = int(self.quantum_entry.get())
                if q <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Time quantum must be a positive integer.")
                return
            result, gantt = round_robin(processes, q)
        elif algo == "pri":
            result = priority_non_preemptive(processes)
            gantt  = build_gantt_from_result(result)

        self.result_data = result
        self.gantt_data  = gantt or []

        self._draw_gantt(gantt or [])
        self._populate_table(result)
        self._show_stats(result)

    # ── Gantt chart ────────────────────────────────────────────────────────────

    def _draw_gantt(self, gantt):
        c = self.gantt_canvas
        c.delete("all")
        if not gantt:
            return

        c.update_idletasks()
        W      = c.winfo_width() or 700
        H      = 100
        pad_x  = 10
        pad_y  = 16
        bar_h  = 44
        y0     = pad_y
        y1     = y0 + bar_h

        total_time = max(g[2] for g in gantt)
        scale = (W - 2 * pad_x) / max(total_time, 1)

        # build pid→color map
        pid_color = {}
        for i, row in enumerate(self.process_rows):
            pid_color[i + 1] = row["color"]

        for pid, start, end in gantt:
            x0 = pad_x + start * scale
            x1 = pad_x + end   * scale
            col = pid_color.get(pid, ACCENT)

            # bar with slight rounded feel via overlapping rectangles
            c.create_rectangle(x0, y0, x1, y1, fill=col, outline="", width=0)
            c.create_rectangle(x0, y0, x1, y0 + 4, fill=self._lighten(col), outline="")
            c.create_line(x0, y0, x1, y0, fill=self._lighten(col), width=2)

            # label
            mid = (x0 + x1) / 2
            if x1 - x0 > 18:
                c.create_text(mid, (y0 + y1) / 2, text=f"P{pid}",
                              font=("Courier New", 8, "bold"), fill=BG)

            # tick marks
            c.create_line(x0, y1, x0, y1 + 6, fill=SUBTEXT, width=1)
            c.create_text(x0, y1 + 14, text=str(start),
                          font=("Courier New", 7), fill=SUBTEXT)

        # final tick
        x_end = pad_x + total_time * scale
        c.create_line(x_end, y1, x_end, y1 + 6, fill=SUBTEXT)
        c.create_text(x_end, y1 + 14, text=str(total_time),
                      font=("Courier New", 7), fill=SUBTEXT)

    def _lighten(self, hex_color):
        """Return a brighter version of a hex colour."""
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, r + 60)
        g = min(255, g + 60)
        b = min(255, b + 60)
        return f"#{r:02x}{g:02x}{b:02x}"

    # ── Results table ──────────────────────────────────────────────────────────

    def _populate_table(self, result):
        for item in self.tree.get_children():
            self.tree.delete(item)

        pid_color = {i + 1: row["color"] for i, row in enumerate(self.process_rows)}

        for r in result:
            pid, arr, burst, wt, tat = r
            rr = round((tat) / burst, 2) if burst else "–"
            tag = f"p{pid}"
            self.tree.insert("", "end",
                             values=(f"P{pid}", arr, burst, wt, tat, rr),
                             tags=(tag,))
            col = pid_color.get(pid, ACCENT)
            self.tree.tag_configure(tag, foreground=col)

    # ── Summary stats ──────────────────────────────────────────────────────────

    def _show_stats(self, result):
        for w in self.stats_frame.winfo_children():
            w.destroy()

        wts  = [r[3] for r in result]
        tats = [r[4] for r in result]
        avg_wt  = sum(wts)  / len(wts)
        avg_tat = sum(tats) / len(tats)
        cpu_util = sum(r[2] for r in result) / max(r[4] + r[1] for r in result) * 100 \
                   if result else 0

        stats = [
            ("Avg Waiting Time",     f"{avg_wt:.2f}",    WARN),
            ("Avg Turnaround Time",  f"{avg_tat:.2f}",   BLUE),
            ("CPU Utilization",      f"{cpu_util:.1f}%", GREEN),
            ("Processes",            str(len(result)),   ACCENT),
        ]
        for label, value, color in stats:
            card = tk.Frame(self.stats_frame, bg=CARD, padx=14, pady=8)
            card.pack(side="left", padx=(0, 8), pady=4)
            tk.Label(card, text=value, font=("Courier New", 18, "bold"),
                     bg=CARD, fg=color).pack()
            tk.Label(card, text=label, font=FONT_SMALL,
                     bg=CARD, fg=SUBTEXT).pack()


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerApp(root)
    root.mainloop()