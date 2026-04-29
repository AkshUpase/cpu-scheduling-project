"""CPU Scheduling Tab — FCFS, SJF, SRTF, RR, Priority, MLQ, MLFQ with Gantt chart."""
import customtkinter as ctk
from tkinter import messagebox
import random, csv, os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms import (fcfs, sjf, srtf, round_robin, priority_scheduling,
                         multilevel_queue, mlfq, generate_random_processes)

ACCENT = "#00d4aa"; ACCENT2 = "#7c3aed"; BG = "#0d1117"; PANEL = "#161b22"
CARD = "#1c2230"; BORDER = "#30363d"; TEXT = "#e6edf3"; SUBTEXT = "#8b949e"
COLORS = ["#00d4aa","#7c3aed","#f59e0b","#f87171","#4ade80","#60a5fa","#f472b6","#fb923c","#34d399","#a78bfa"]

class CPUTab:
    def __init__(self, parent):
        self.parent = parent
        self.rows = []
        self._build()

    def _build(self):
        main = ctk.CTkFrame(self.parent, fg_color=BG)
        main.pack(fill="both", expand=True)

        # Left panel
        left = ctk.CTkFrame(main, fg_color=PANEL, width=320, corner_radius=0)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        ctk.CTkLabel(left, text="ALGORITHM", font=ctk.CTkFont("Consolas", 11, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(12,4))

        self.algo_var = ctk.StringVar(value="fcfs")
        algos = [("FCFS", "fcfs"), ("SJF (Non-Preemptive)", "sjf"),
                 ("SRTF (Preemptive)", "srtf"), ("Round Robin", "rr"),
                 ("Priority", "pri"), ("Multilevel Queue", "mlq"),
                 ("MLFQ ⭐", "mlfq")]
        for label, val in algos:
            ctk.CTkRadioButton(left, text=label, variable=self.algo_var, value=val,
                               font=ctk.CTkFont("Consolas", 11), text_color=TEXT,
                               fg_color=ACCENT, hover_color=ACCENT2,
                               command=self._on_algo_change).pack(anchor="w", padx=20, pady=2)

        # Quantum frame
        self.q_frame = ctk.CTkFrame(left, fg_color=PANEL)
        ctk.CTkLabel(self.q_frame, text="Quantum:", font=ctk.CTkFont("Consolas", 11),
                     text_color=SUBTEXT).pack(side="left", padx=(0,8))
        self.q_entry = ctk.CTkEntry(self.q_frame, width=50, font=ctk.CTkFont("Consolas", 11))
        self.q_entry.insert(0, "2")
        self.q_entry.pack(side="left")

        # Separator
        ctk.CTkFrame(left, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(left, text="PROCESSES", font=ctk.CTkFont("Consolas", 11, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(4,4))

        ctrl = ctk.CTkFrame(left, fg_color=PANEL)
        ctrl.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(ctrl, text="Count:", font=ctk.CTkFont("Consolas", 11),
                     text_color=SUBTEXT).pack(side="left")
        self.n_entry = ctk.CTkEntry(ctrl, width=40, font=ctk.CTkFont("Consolas", 11))
        self.n_entry.insert(0, "5")
        self.n_entry.pack(side="left", padx=8)
        ctk.CTkButton(ctrl, text="Generate", width=70, fg_color=ACCENT2,
                       hover_color="#6d28d9", font=ctk.CTkFont("Consolas", 10),
                       command=self._gen).pack(side="left", padx=4)
        ctk.CTkButton(ctrl, text="🎲 Random", width=70, fg_color="#f59e0b",
                       hover_color="#d97706", font=ctk.CTkFont("Consolas", 10),
                       text_color=BG, command=self._random).pack(side="left", padx=4)

        # Header row
        hdr = ctk.CTkFrame(left, fg_color=CARD, corner_radius=4)
        hdr.pack(fill="x", padx=16, pady=(8,0))
        for col, w in [("PID",4),("AT",5),("BT",5),("Pri",4)]:
            ctk.CTkLabel(hdr, text=col, font=ctk.CTkFont("Consolas", 9, "bold"),
                         text_color=SUBTEXT, width=w*8).pack(side="left", padx=4, pady=4)

        self.proc_scroll = ctk.CTkScrollableFrame(left, fg_color=PANEL, height=200)
        self.proc_scroll.pack(fill="x", padx=16, pady=4)

        ctk.CTkFrame(left, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=8)

        ctk.CTkButton(left, text="▶  RUN SIMULATION", fg_color=ACCENT, text_color=BG,
                       hover_color="#00b894", font=ctk.CTkFont("Consolas", 13, "bold"),
                       height=42, command=self._run).pack(fill="x", padx=16, pady=4)

        btn_row = ctk.CTkFrame(left, fg_color=PANEL)
        btn_row.pack(fill="x", padx=16, pady=4)
        ctk.CTkButton(btn_row, text="✕ Clear", fg_color=CARD, hover_color=BORDER,
                       text_color=SUBTEXT, font=ctk.CTkFont("Consolas", 10),
                       command=self._clear).pack(side="left", expand=True, fill="x", padx=(0,4))
        ctk.CTkButton(btn_row, text="💾 Export CSV", fg_color=CARD, hover_color=BORDER,
                       text_color=SUBTEXT, font=ctk.CTkFont("Consolas", 10),
                       command=self._export).pack(side="left", expand=True, fill="x", padx=(4,0))

        # Right panel
        right = ctk.CTkFrame(main, fg_color=BG)
        right.pack(side="right", fill="both", expand=True)

        # Stats
        self.stats_frame = ctk.CTkFrame(right, fg_color=BG)
        self.stats_frame.pack(fill="x", padx=16, pady=(12,0))

        # Analysis
        self.analysis_label = ctk.CTkLabel(right, text="", font=ctk.CTkFont("Consolas", 11),
                                            text_color="#4ade80", wraplength=700, justify="left")
        self.analysis_label.pack(fill="x", padx=16, pady=(4,0))

        # Gantt
        ctk.CTkLabel(right, text="GANTT CHART", font=ctk.CTkFont("Consolas", 10, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(10,2))

        from tkinter import Canvas
        self.gantt_canvas = Canvas(right, bg=CARD, height=90, highlightthickness=0, bd=0)
        self.gantt_canvas.pack(fill="x", padx=16, pady=(0,4))

        # Results table
        ctk.CTkLabel(right, text="RESULTS TABLE", font=ctk.CTkFont("Consolas", 10, "bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))

        self.table_frame = ctk.CTkScrollableFrame(right, fg_color=CARD, height=250)
        self.table_frame.pack(fill="both", expand=True, padx=16, pady=(0,12))

        self.last_result = None

    def _on_algo_change(self):
        algo = self.algo_var.get()
        if algo in ("rr", "mlfq"):
            self.q_frame.pack(fill="x", padx=20, pady=4)
        else:
            self.q_frame.pack_forget()

    def _gen(self):
        for w in self.proc_scroll.winfo_children():
            w.destroy()
        self.rows.clear()
        try:
            n = int(self.n_entry.get())
            assert 1 <= n <= 15
        except:
            messagebox.showerror("Error", "Enter 1–15"); return
        for i in range(n):
            self._add_row(i, str(i), str(random.randint(1,8)), str(random.randint(1,3)))

    def _random(self):
        try:
            n = int(self.n_entry.get())
        except:
            n = 5
        procs = generate_random_processes(n)
        for w in self.proc_scroll.winfo_children():
            w.destroy()
        self.rows.clear()
        for pid, at, bt, pri in procs:
            self._add_row(pid-1, str(at), str(bt), str(pri))

    def _add_row(self, i, at, bt, pri):
        color = COLORS[i % len(COLORS)]
        row = ctk.CTkFrame(self.proc_scroll, fg_color=PANEL)
        row.pack(fill="x", pady=1)
        ctk.CTkLabel(row, text=f"P{i+1}", font=ctk.CTkFont("Consolas", 9, "bold"),
                     text_color=BG, fg_color=color, width=35, corner_radius=4).pack(side="left", padx=2)
        e_at = ctk.CTkEntry(row, width=45, font=ctk.CTkFont("Consolas", 10)); e_at.insert(0, at); e_at.pack(side="left", padx=2)
        e_bt = ctk.CTkEntry(row, width=45, font=ctk.CTkFont("Consolas", 10)); e_bt.insert(0, bt); e_bt.pack(side="left", padx=2)
        e_pri = ctk.CTkEntry(row, width=40, font=ctk.CTkFont("Consolas", 10)); e_pri.insert(0, pri); e_pri.pack(side="left", padx=2)
        self.rows.append({"at": e_at, "bt": e_bt, "pri": e_pri, "color": color})

    def _run(self):
        if not self.rows:
            messagebox.showwarning("No Data", "Generate processes first."); return
        algo = self.algo_var.get()
        processes = []
        for i, r in enumerate(self.rows):
            try:
                at = int(r["at"].get()); bt = int(r["bt"].get()); pri = int(r["pri"].get())
                assert at >= 0 and bt > 0
                processes.append((i+1, at, bt, pri))
            except:
                messagebox.showerror("Error", f"Invalid P{i+1}"); return

        try:
            q = int(self.q_entry.get()) if algo in ("rr","mlfq") else 2
        except:
            q = 2

        funcs = {
            "fcfs": lambda: fcfs(processes),
            "sjf": lambda: sjf(processes),
            "srtf": lambda: srtf(processes),
            "rr": lambda: round_robin(processes, q),
            "pri": lambda: priority_scheduling(processes),
            "mlq": lambda: multilevel_queue(processes, q),
            "mlfq": lambda: mlfq(processes, max(1, q//2), q),
        }
        result, gantt = funcs[algo]()
        self.last_result = result
        self._draw_gantt(gantt)
        self._draw_table(result)
        self._draw_stats(result)

    def _draw_gantt(self, gantt):
        c = self.gantt_canvas
        c.delete("all")
        if not gantt: return
        c.update_idletasks()
        W = max(c.winfo_width(), 600)
        pad, bar_h = 10, 44
        y0, y1 = 14, 14 + bar_h
        total = max(g[2] for g in gantt)
        scale = (W - 2*pad) / max(total, 1)
        pid_col = {i+1: r["color"] for i, r in enumerate(self.rows)}

        for pid, start, end in gantt:
            x0 = pad + start * scale
            x1 = pad + end * scale
            col = pid_col.get(pid, ACCENT)
            c.create_rectangle(x0, y0, x1, y1, fill=col, outline="")
            if x1 - x0 > 18:
                c.create_text((x0+x1)/2, (y0+y1)/2, text=f"P{pid}",
                              font=("Consolas", 8, "bold"), fill=BG)
            c.create_line(x0, y1, x0, y1+5, fill=SUBTEXT)
            c.create_text(x0, y1+13, text=str(start), font=("Consolas", 7), fill=SUBTEXT)

        x_end = pad + total * scale
        c.create_line(x_end, y1, x_end, y1+5, fill=SUBTEXT)
        c.create_text(x_end, y1+13, text=str(total), font=("Consolas", 7), fill=SUBTEXT)

    def _draw_table(self, result):
        for w in self.table_frame.winfo_children():
            w.destroy()
        hdr = ctk.CTkFrame(self.table_frame, fg_color=PANEL)
        hdr.pack(fill="x", pady=(0,4))
        for col in ["PID","Arrival","Burst","Waiting","Turnaround","Response Ratio"]:
            ctk.CTkLabel(hdr, text=col, font=ctk.CTkFont("Consolas", 10, "bold"),
                         text_color=ACCENT, width=100).pack(side="left", padx=4)
        for r in result:
            pid, at, bt, wt, tat = r
            rr = f"{tat/bt:.2f}" if bt else "–"
            row = ctk.CTkFrame(self.table_frame, fg_color=CARD)
            row.pack(fill="x", pady=1)
            col = COLORS[(pid-1) % len(COLORS)]
            for val in [f"P{pid}", at, bt, wt, tat, rr]:
                ctk.CTkLabel(row, text=str(val), font=ctk.CTkFont("Consolas", 10),
                             text_color=col, width=100).pack(side="left", padx=4)

    def _draw_stats(self, result):
        for w in self.stats_frame.winfo_children():
            w.destroy()
        wts = [r[3] for r in result]
        tats = [r[4] for r in result]
        avg_wt = sum(wts)/len(wts)
        avg_tat = sum(tats)/len(tats)
        total_burst = sum(r[2] for r in result)
        makespan = max(r[1]+r[4] for r in result)
        cpu_util = (total_burst / makespan * 100) if makespan else 0

        stats = [("Avg WT", f"{avg_wt:.2f}", "#f59e0b"),
                 ("Avg TAT", f"{avg_tat:.2f}", "#60a5fa"),
                 ("CPU Util", f"{cpu_util:.1f}%", "#4ade80"),
                 ("Processes", str(len(result)), ACCENT)]
        for label, val, col in stats:
            card = ctk.CTkFrame(self.stats_frame, fg_color=CARD, corner_radius=8)
            card.pack(side="left", padx=(0,8), pady=4)
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont("Consolas", 20, "bold"),
                         text_color=col).pack(padx=14, pady=(8,0))
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont("Consolas", 9),
                         text_color=SUBTEXT).pack(padx=14, pady=(0,8))

        # Auto analysis
        best_p = min(result, key=lambda r: r[3])
        worst_p = max(result, key=lambda r: r[3])
        algo_name = self.algo_var.get().upper()
        self.analysis_label.configure(
            text=f"📊 Analysis: Avg WT={avg_wt:.2f} | Avg TAT={avg_tat:.2f} | "
                 f"Best: P{best_p[0]} (WT={best_p[3]}) | Worst: P{worst_p[0]} (WT={worst_p[3]})")

    def _clear(self):
        for w in self.proc_scroll.winfo_children(): w.destroy()
        self.rows.clear()
        self.gantt_canvas.delete("all")
        for w in self.table_frame.winfo_children(): w.destroy()
        for w in self.stats_frame.winfo_children(): w.destroy()
        self.analysis_label.configure(text="")
        self.last_result = None

    def _export(self):
        if not self.last_result:
            messagebox.showinfo("No Data", "Run a simulation first."); return
        path = os.path.join(os.path.dirname(__file__), "..", "output", "cpu_results.csv")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["PID","Arrival","Burst","Waiting","Turnaround"])
            for r in self.last_result:
                w.writerow([f"P{r[0]}", r[1], r[2], r[3], r[4]])
        messagebox.showinfo("Exported", f"Saved to {os.path.abspath(path)}")
