import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

# ── Palette ────────────────────────────────────────────────────────────────────
BG       = "#0d1117"
PANEL    = "#161b22"
CARD     = "#1c2230"
BORDER   = "#30363d"
ACCENT   = "#00d4aa"
ACCENT2  = "#7c3aed"
WARN     = "#f59e0b"
TEXT     = "#e6edf3"
SUBTEXT  = "#8b949e"
GREEN    = "#4ade80"
BLUE     = "#60a5fa"
#this is the code for color
PROCESS_COLORS = ["#00d4aa","#7c3aed","#f59e0b","#f87171",
                  "#4ade80","#60a5fa","#f472b6","#fb923c",
                  "#34d399","#a78bfa"]

FONT_TITLE = ("Courier New", 20, "bold")
FONT_HEAD  = ("Courier New", 11, "bold")
FONT_BODY  = ("Courier New", 10)
FONT_SMALL = ("Courier New", 9)
FONT_MONO  = ("Courier New", 10)

# Path to your compiled executable (adjust if needed)
SCHEDULER_EXE = os.path.join(os.path.dirname(__file__), "..", "scheduler.exe")


class CPUSchedulerUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1080x760")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)
        self.process_rows = []
        self._build_ui()

    # ── UI Build ───────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=PANEL, height=62)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="⚙  CPU SCHEDULING SIMULATOR",
                 font=FONT_TITLE, bg=PANEL, fg=ACCENT).pack(side="left", padx=24, pady=12)
        tk.Label(hdr, text="OS Project  •  FCFS Module",
                 font=FONT_SMALL, bg=PANEL, fg=SUBTEXT).pack(side="right", padx=24)
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill="x")

        # Body
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)
        self._left_panel(body).pack(side="left", fill="y")
        self._right_panel(body).pack(side="right", fill="both", expand=True)

    # ── Left Panel ─────────────────────────────────────────────────────────────

    def _left_panel(self, parent):
        f = tk.Frame(parent, bg=PANEL, width=300)
        f.pack_propagate(False)

        # Algorithm badge (FCFS only for now)
        self._section(f, "ALGORITHM")
        badge = tk.Frame(f, bg=CARD, padx=12, pady=8)
        badge.pack(fill="x", padx=16, pady=(0, 4))
        tk.Label(badge, text="● FCFS  —  First Come First Served",
                 font=FONT_BODY, bg=CARD, fg=ACCENT).pack(anchor="w")
        tk.Label(badge, text="Non-preemptive  |  Order by Arrival Time",
                 font=FONT_SMALL, bg=CARD, fg=SUBTEXT).pack(anchor="w", pady=(2, 0))

        self._divider(f)
        self._section(f, "PROCESSES")

        # Count row
        cr = tk.Frame(f, bg=PANEL)
        cr.pack(fill="x", padx=16, pady=4)
        tk.Label(cr, text="Count (1–10):", font=FONT_BODY,
                 bg=PANEL, fg=SUBTEXT).pack(side="left")
        self.num_entry = self._entry(cr, width=4)
        self.num_entry.insert(0, "4")
        self.num_entry.pack(side="left", padx=8)
        self._btn(cr, "Generate", self._create_inputs, ACCENT2).pack(side="left")

        # Column headers
        hdr = tk.Frame(f, bg=CARD)
        hdr.pack(fill="x", padx=16, pady=(8, 0))
        for col, w in [("", 4), ("Arrival", 8), ("Burst", 7)]:
            tk.Label(hdr, text=col, font=FONT_SMALL, bg=CARD, fg=SUBTEXT,
                     width=w, anchor="center").pack(side="left", padx=2, pady=4)

        self.proc_frame = tk.Frame(f, bg=PANEL)
        self.proc_frame.pack(fill="x", padx=16)

        self._divider(f)

        # Run button
        tk.Button(f, text="▶  RUN FCFS",
                  font=("Courier New", 12, "bold"),
                  bg=ACCENT, fg=BG, relief="flat",
                  activebackground="#00b894", activeforeground=BG,
                  cursor="hand2", pady=10,
                  command=self._run).pack(fill="x", padx=16, pady=6)

        tk.Button(f, text="✕  Clear",
                  font=FONT_SMALL, bg=CARD, fg=SUBTEXT,
                  relief="flat", cursor="hand2", pady=6,
                  command=self._clear).pack(fill="x", padx=16, pady=(0, 8))

        return f

    # ── Right Panel ────────────────────────────────────────────────────────────

    def _right_panel(self, parent):
        f = tk.Frame(parent, bg=BG)

        # Stats row
        self.stats_frame = tk.Frame(f, bg=BG)
        self.stats_frame.pack(fill="x", padx=16, pady=(12, 0))

        # Gantt
        self._section_lbl(f, "GANTT CHART")
        self.gantt_canvas = tk.Canvas(f, bg=CARD, height=96, highlightthickness=0)
        self.gantt_canvas.pack(fill="x", padx=16, pady=(4, 0))

        # Results table
        self._section_lbl(f, "RESULTS TABLE")
        tbl = tk.Frame(f, bg=CARD)
        tbl.pack(fill="both", expand=True, padx=16, pady=(4, 16))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("S.Treeview", background=CARD, foreground=TEXT,
                        fieldbackground=CARD, borderwidth=0,
                        font=FONT_MONO, rowheight=28)
        style.configure("S.Treeview.Heading", background=PANEL,
                        foreground=ACCENT, font=FONT_HEAD, relief="flat")
        style.map("S.Treeview", background=[("selected", ACCENT2)])

        cols = ("PID", "Arrival", "Burst", "Waiting", "Turnaround")
        self.tree = ttk.Treeview(tbl, columns=cols, show="headings",
                                  style="S.Treeview")
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=130)

        vsb = ttk.Scrollbar(tbl, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Raw output log
        self._section_lbl(f, "RAW OUTPUT  (scheduler.exe)")
        self.log = tk.Text(f, height=6, bg=CARD, fg=SUBTEXT,
                           font=FONT_SMALL, relief="flat",
                           insertbackground=ACCENT, state="disabled")
        self.log.pack(fill="x", padx=16, pady=(4, 12))

        return f

    # ── Process row generation ─────────────────────────────────────────────────

    def _create_inputs(self):
        for w in self.proc_frame.winfo_children():
            w.destroy()
        self.process_rows.clear()
        try:
            n = int(self.num_entry.get())
            assert 1 <= n <= 10
        except Exception:
            messagebox.showerror("Error", "Enter a number between 1 and 10.")
            return

        for i in range(n):
            color = PROCESS_COLORS[i % len(PROCESS_COLORS)]
            row = tk.Frame(self.proc_frame, bg=PANEL)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=f"P{i+1}", font=("Courier New", 9, "bold"),
                     bg=color, fg=BG, width=4).pack(side="left", padx=(0, 4))

            arr = self._entry(row, width=7)
            arr.pack(side="left", padx=2)
            arr.insert(0, str(i))

            bst = self._entry(row, width=6)
            bst.pack(side="left", padx=2)
            bst.insert(0, str(5 - i % 4))

            self.process_rows.append({"arrival": arr, "burst": bst, "color": color, "idx": i+1})

    # ── Run FCFS via scheduler.exe ─────────────────────────────────────────────

    def _run(self):
        if not self.process_rows:
            messagebox.showwarning("No Processes", "Click Generate first.")
            return

        # Build input string for the C program
        # Format expected by input.c: first line = n, then "arrival burst" per line
        lines = [str(len(self.process_rows))]
        for row in self.process_rows:
            try:
                arr = int(row["arrival"].get())
                bst = int(row["burst"].get())
                assert arr >= 0 and bst > 0
            except Exception:
                messagebox.showerror("Input Error",
                    f"Invalid values for P{row['idx']}. Arrival ≥ 0, Burst > 0.")
                return
            lines.append(f"{arr} {bst}")
        stdin_data = "\n".join(lines) + "\n"

        # Call scheduler.exe
        exe = SCHEDULER_EXE
        if not os.path.isfile(exe):
            # Try current directory fallback
            exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scheduler.exe")
        if not os.path.isfile(exe):
            messagebox.showerror("Not Found",
                f"scheduler.exe not found.\nExpected: {exe}\n\nRun 'make' first.")
            return

        try:
            proc = subprocess.run(
                [exe],
                input=stdin_data,
                capture_output=True,
                text=True,
                timeout=5
            )
            raw = proc.stdout.strip()
        except subprocess.TimeoutExpired:
            messagebox.showerror("Timeout", "scheduler.exe timed out.")
            return
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        # Show raw output in log
        self._set_log(raw if raw else "(no output)")

        # Parse output — expected format per line:
        # PID  ArrivalTime  BurstTime  WaitingTime  TurnaroundTime
        result = []
        for line in raw.splitlines():
            parts = line.split()
            if len(parts) >= 5:
                try:
                    pid = int(parts[0])
                    arr = int(parts[1])
                    bst = int(parts[2])
                    wt  = int(parts[3])
                    tat = int(parts[4])
                    result.append((pid, arr, bst, wt, tat))
                except ValueError:
                    continue  # skip header lines

        if not result:
            return  # nothing parseable, raw log already shown

        self._draw_gantt(result)
        self._populate_table(result)
        self._show_stats(result)

    # ── Gantt ──────────────────────────────────────────────────────────────────

    def _draw_gantt(self, result):
        c = self.gantt_canvas
        c.delete("all")
        c.update_idletasks()
        W = c.winfo_width() or 700
        pad_x, pad_y, bar_h = 10, 14, 44
        y0, y1 = pad_y, pad_y + bar_h

        total = max(r[1] + r[4] for r in result)  # arrival + TAT = finish
        scale = (W - 2 * pad_x) / max(total, 1)

        pid_color = {row["idx"]: row["color"] for row in self.process_rows}

        for pid, arr, bst, wt, tat in result:
            start = arr + wt
            end   = start + bst
            x0 = pad_x + start * scale
            x1 = pad_x + end   * scale
            col = pid_color.get(pid, ACCENT)

            c.create_rectangle(x0, y0, x1, y1, fill=col, outline="")
            c.create_rectangle(x0, y0, x1, y0 + 4,
                               fill=self._lighten(col), outline="")
            if x1 - x0 > 16:
                c.create_text((x0+x1)/2, (y0+y1)/2,
                               text=f"P{pid}",
                               font=("Courier New", 8, "bold"), fill=BG)
            c.create_line(x0, y1, x0, y1+5, fill=SUBTEXT)
            c.create_text(x0, y1+13, text=str(start),
                          font=("Courier New", 7), fill=SUBTEXT)

        x_end = pad_x + total * scale
        c.create_line(x_end, y1, x_end, y1+5, fill=SUBTEXT)
        c.create_text(x_end, y1+13, text=str(total),
                      font=("Courier New", 7), fill=SUBTEXT)

    # ── Table ──────────────────────────────────────────────────────────────────

    def _populate_table(self, result):
        for item in self.tree.get_children():
            self.tree.delete(item)
        pid_color = {row["idx"]: row["color"] for row in self.process_rows}
        for pid, arr, bst, wt, tat in result:
            tag = f"p{pid}"
            self.tree.insert("", "end",
                             values=(f"P{pid}", arr, bst, wt, tat),
                             tags=(tag,))
            self.tree.tag_configure(tag, foreground=pid_color.get(pid, ACCENT))

    # ── Stats ──────────────────────────────────────────────────────────────────

    def _show_stats(self, result):
        for w in self.stats_frame.winfo_children():
            w.destroy()
        wts  = [r[3] for r in result]
        tats = [r[4] for r in result]
        stats = [
            ("Avg Waiting Time",    f"{sum(wts)/len(wts):.2f}",   WARN),
            ("Avg Turnaround Time", f"{sum(tats)/len(tats):.2f}", BLUE),
            ("Processes",           str(len(result)),              ACCENT),
        ]
        for label, val, col in stats:
            card = tk.Frame(self.stats_frame, bg=CARD, padx=14, pady=8)
            card.pack(side="left", padx=(0, 8))
            tk.Label(card, text=val, font=("Courier New", 18, "bold"),
                     bg=CARD, fg=col).pack()
            tk.Label(card, text=label, font=FONT_SMALL,
                     bg=CARD, fg=SUBTEXT).pack()

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _clear(self):
        for w in self.proc_frame.winfo_children():
            w.destroy()
        self.process_rows.clear()
        self.gantt_canvas.delete("all")
        for item in self.tree.get_children():
            self.tree.delete(item)
        for w in self.stats_frame.winfo_children():
            w.destroy()
        self._set_log("")

    def _set_log(self, text):
        self.log.configure(state="normal")
        self.log.delete("1.0", tk.END)
        self.log.insert(tk.END, text)
        self.log.configure(state="disabled")

    def _section(self, parent, text):
        f = tk.Frame(parent, bg=PANEL)
        f.pack(fill="x", padx=16, pady=(12, 4))
        tk.Label(f, text=text, font=("Courier New", 9, "bold"),
                 bg=PANEL, fg=ACCENT).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(8, 0), pady=6)

    def _section_lbl(self, parent, text):
        f = tk.Frame(parent, bg=BG)
        f.pack(fill="x", padx=16, pady=(10, 2))
        tk.Label(f, text=text, font=("Courier New", 9, "bold"),
                 bg=BG, fg=ACCENT).pack(side="left")
        tk.Frame(f, bg=BORDER, height=1).pack(
            side="left", fill="x", expand=True, padx=(8, 0), pady=6)

    def _divider(self, parent):
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=16, pady=8)

    def _entry(self, parent, width=8):
        return tk.Entry(parent, width=width, bg=CARD, fg=TEXT,
                        insertbackground=ACCENT, relief="flat",
                        font=FONT_BODY, highlightthickness=1,
                        highlightcolor=ACCENT, highlightbackground=BORDER)

    def _btn(self, parent, text, cmd, color=ACCENT):
        return tk.Button(parent, text=text, command=cmd,
                         bg=color, fg=BG, font=FONT_SMALL,
                         relief="flat", padx=8, pady=4, cursor="hand2")

    def _lighten(self, hex_color):
        h = hex_color.lstrip("#")
        r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
        return f"#{min(255,r+60):02x}{min(255,g+60):02x}{min(255,b+60):02x}"


# ── Entry ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    CPUSchedulerUI(root)
    root.mainloop()
