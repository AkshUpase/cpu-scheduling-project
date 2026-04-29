"""Compare Tab — Compare all CPU scheduling algorithms side-by-side with graphs."""
import customtkinter as ctk
from tkinter import Canvas, messagebox
import os, sys, csv, random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms import compare_cpu_algorithms, generate_random_processes

ACCENT="#00d4aa"; ACCENT2="#7c3aed"; BG="#0d1117"; PANEL="#161b22"
CARD="#1c2230"; BORDER="#30363d"; TEXT="#e6edf3"; SUBTEXT="#8b949e"
ALGO_COLORS={"FCFS":"#00d4aa","SJF":"#7c3aed","SRTF":"#f59e0b","Round Robin":"#f87171",
             "Priority":"#4ade80","MLFQ":"#60a5fa"}

class CompareTab:
    def __init__(self, parent):
        self.parent = parent
        self._build()

    def _build(self):
        main = ctk.CTkFrame(self.parent, fg_color=BG)
        main.pack(fill="both", expand=True)

        top = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=0)
        top.pack(fill="x")

        ctk.CTkLabel(top, text="📊 ALGORITHM COMPARISON MODE",
                     font=ctk.CTkFont("Consolas",14,"bold"), text_color=ACCENT).pack(side="left", padx=16, pady=12)

        ctrl = ctk.CTkFrame(top, fg_color=PANEL)
        ctrl.pack(side="right", padx=16, pady=8)
        ctk.CTkLabel(ctrl, text="Processes:", font=ctk.CTkFont("Consolas",10),
                     text_color=SUBTEXT).pack(side="left")
        self.n_entry = ctk.CTkEntry(ctrl, width=40, font=ctk.CTkFont("Consolas",10))
        self.n_entry.insert(0, "6"); self.n_entry.pack(side="left", padx=4)
        ctk.CTkLabel(ctrl, text="Quantum:", font=ctk.CTkFont("Consolas",10),
                     text_color=SUBTEXT).pack(side="left", padx=(8,0))
        self.q_entry = ctk.CTkEntry(ctrl, width=40, font=ctk.CTkFont("Consolas",10))
        self.q_entry.insert(0, "2"); self.q_entry.pack(side="left", padx=4)
        ctk.CTkButton(ctrl, text="🎲 Random & Compare", fg_color=ACCENT, text_color=BG,
                       hover_color="#00b894", font=ctk.CTkFont("Consolas",11,"bold"),
                       command=self._run).pack(side="left", padx=8)
        ctk.CTkButton(ctrl, text="💾 Export", fg_color=CARD, text_color=SUBTEXT,
                       hover_color=BORDER, font=ctk.CTkFont("Consolas",10),
                       command=self._export).pack(side="left", padx=4)

        # Analysis banner
        self.analysis = ctk.CTkLabel(main, text="", font=ctk.CTkFont("Consolas", 11),
                                      text_color="#4ade80", wraplength=900)
        self.analysis.pack(fill="x", padx=16, pady=(8, 0))

        # ── Three bar charts ──────────────────────────────────────────────────
        charts = ctk.CTkFrame(main, fg_color=BG)
        charts.pack(fill="x", padx=16, pady=(8, 4))
        charts.columnconfigure(0, weight=1)
        charts.columnconfigure(1, weight=1)
        charts.columnconfigure(2, weight=1)

        for col_idx, (title, attr) in enumerate([
            ("AVG WAITING TIME",    "wt_canvas"),
            ("AVG TURNAROUND TIME", "tat_canvas"),
            ("CONTEXT SWITCHES",    "ctx_canvas"),
        ]):
            frame = ctk.CTkFrame(charts, fg_color=BG)
            frame.grid(row=0, column=col_idx, padx=4, sticky="nsew")
            ctk.CTkLabel(frame, text=title,
                         font=ctk.CTkFont("Consolas", 9, "bold"),
                         text_color=ACCENT).pack(anchor="w", pady=(0, 2))
            canvas = Canvas(frame, bg=CARD, height=160, highlightthickness=0)
            canvas.pack(fill="x")
            setattr(self, attr, canvas)

        # Table
        self.table_frame = ctk.CTkScrollableFrame(main, fg_color=CARD, height=160)
        self.table_frame.pack(fill="both", expand=True, padx=16, pady=(4, 12))

        self.last_results = None

    def _run(self):
        try:
            n = int(self.n_entry.get())
            q = int(self.q_entry.get())
        except Exception:
            n, q = 6, 2
        procs = generate_random_processes(n)
        results = compare_cpu_algorithms(procs, q)
        self.last_results = results

        if not results:
            return

        best_wt  = min(results.items(), key=lambda x: x[1]['avg_wt'])
        worst_wt = max(results.items(), key=lambda x: x[1]['avg_wt'])
        best_tat = min(results.items(), key=lambda x: x[1]['avg_tat'])
        best_ctx = min(results.items(), key=lambda x: x[1]['context_switches'])

        self.analysis.configure(
            text=(f"🏆 Best WT: {best_wt[0]} ({best_wt[1]['avg_wt']:.2f})  |  "
                  f"❌ Worst WT: {worst_wt[0]} ({worst_wt[1]['avg_wt']:.2f})  |  "
                  f"⚡ Lowest TAT: {best_tat[0]} ({best_tat[1]['avg_tat']:.2f})  |  "
                  f"🔄 Fewest Ctx-Sw: {best_ctx[0]} ({best_ctx[1]['context_switches']})"))

        self._draw_bars(self.wt_canvas,  {k: v['avg_wt']          for k, v in results.items()}, "WT")
        self._draw_bars(self.tat_canvas, {k: v['avg_tat']          for k, v in results.items()}, "TAT")
        self._draw_bars(self.ctx_canvas, {k: v['context_switches'] for k, v in results.items()},
                        "Ctx-Sw", lower_is_better=True, integer_vals=True)
        self._draw_table(results)

    def _draw_bars(self, canvas, data, label,
                   lower_is_better=True, integer_vals=False):
        c = canvas
        c.delete("all")
        c.update_idletasks()
        W = max(c.winfo_width(), 300)
        H = 155
        pad_x, pad_y = 10, 16
        n = len(data)
        if n == 0:
            return
        max_val  = max(data.values()) or 1
        bar_w    = (W - 2 * pad_x) / (n * 2)
        best_key = min(data, key=data.get) if lower_is_better else max(data, key=data.get)

        for i, (name, val) in enumerate(data.items()):
            x0 = pad_x + i * 2 * bar_w + bar_w * 0.3
            x1 = x0 + bar_w * 1.4
            bh = (val / max_val) * (H - 2 * pad_y - 22)
            y0 = H - pad_y - 22 - bh
            y1 = H - pad_y - 22
            col = ALGO_COLORS.get(name, ACCENT)
            if name == best_key:
                c.create_rectangle(x0 - 2, y0 - 2, x1 + 2, y1 + 2,
                                   fill="#4ade80", outline="")
            c.create_rectangle(x0, y0, x1, y1, fill=col, outline="")
            val_str = str(int(val)) if integer_vals else f"{val:.2f}"
            c.create_text((x0 + x1) / 2, y0 - 7,
                          text=val_str, font=("Consolas", 7, "bold"), fill=TEXT)
            # Abbreviated name
            short = name.replace("Round Robin", "RR").replace("Priority", "Pri")
            c.create_text((x0 + x1) / 2, H - pad_y - 8,
                          text=short, font=("Consolas", 7), fill=SUBTEXT)

    def _draw_table(self, results):
        for w in self.table_frame.winfo_children():
            w.destroy()
        hdr = ctk.CTkFrame(self.table_frame, fg_color=PANEL)
        hdr.pack(fill="x", pady=(0, 4))
        cols = ["Algorithm", "Avg WT", "Avg TAT", "Ctx-Sw", "Throughput", "CPU Util%", "Rating"]
        widths = [130, 80, 80, 70, 90, 90, 100]
        for col, w in zip(cols, widths):
            ctk.CTkLabel(hdr, text=col,
                         font=ctk.CTkFont("Consolas", 10, "bold"),
                         text_color=ACCENT, width=w).pack(side="left", padx=2)

        best_key = min(results, key=lambda k: results[k]['avg_wt'])
        for name, data in sorted(results.items(), key=lambda x: x[1]['avg_wt']):
            row = ctk.CTkFrame(self.table_frame, fg_color=CARD)
            row.pack(fill="x", pady=1)
            rating = ("🏆 BEST" if name == best_key
                      else "⭐ Good" if data['avg_wt'] < 5
                      else "⚠️ Slow")
            col = "#4ade80" if name == best_key else SUBTEXT
            row_vals = [
                name,
                f"{data['avg_wt']:.2f}",
                f"{data['avg_tat']:.2f}",
                str(data.get('context_switches', '–')),
                str(data.get('throughput', '–')),
                f"{data.get('cpu_util', 0):.1f}%",
                rating,
            ]
            for val, w in zip(row_vals, widths):
                ctk.CTkLabel(row, text=str(val),
                             font=ctk.CTkFont("Consolas", 10),
                             text_color=col, width=w).pack(side="left", padx=2)

    def _export(self):
        if not self.last_results:
            messagebox.showinfo("No Data", "Run comparison first.")
            return
        path = os.path.join(os.path.dirname(__file__), "..", "..", "output", "comparison.csv")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Algorithm", "Avg WT", "Avg TAT", "Context Switches",
                        "Throughput", "CPU Util%"])
            for name, data in self.last_results.items():
                w.writerow([
                    name,
                    f"{data['avg_wt']:.2f}",
                    f"{data['avg_tat']:.2f}",
                    data.get('context_switches', ''),
                    data.get('throughput', ''),
                    f"{data.get('cpu_util', 0):.1f}",
                ])
        messagebox.showinfo("Exported", f"Saved to {os.path.abspath(path)}")
