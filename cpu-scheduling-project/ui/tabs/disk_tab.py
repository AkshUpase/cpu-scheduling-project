"""Disk Scheduling Tab — FCFS, SSTF, SCAN, C-SCAN with seek graph."""
import customtkinter as ctk
from tkinter import Canvas, messagebox
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms import disk_fcfs, disk_sstf, disk_scan, disk_cscan

ACCENT="#00d4aa"; ACCENT2="#7c3aed"; BG="#0d1117"; PANEL="#161b22"
CARD="#1c2230"; BORDER="#30363d"; TEXT="#e6edf3"; SUBTEXT="#8b949e"
COLORS=["#00d4aa","#7c3aed","#f59e0b","#f87171","#4ade80","#60a5fa"]

class DiskTab:
    def __init__(self, parent):
        self.parent = parent
        self._build()

    def _build(self):
        main = ctk.CTkFrame(self.parent, fg_color=BG)
        main.pack(fill="both", expand=True)

        left = ctk.CTkFrame(main, fg_color=PANEL, width=300, corner_radius=0)
        left.pack(side="left", fill="y"); left.pack_propagate(False)

        ctk.CTkLabel(left, text="ALGORITHM", font=ctk.CTkFont("Consolas",11,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(12,4))
        self.algo_var = ctk.StringVar(value="fcfs")
        for label, val in [("FCFS","fcfs"),("SSTF","sstf"),("SCAN (Elevator)","scan"),
                            ("C-SCAN","cscan")]:
            ctk.CTkRadioButton(left, text=label, variable=self.algo_var, value=val,
                               font=ctk.CTkFont("Consolas",11), text_color=TEXT,
                               fg_color=ACCENT, hover_color=ACCENT2).pack(anchor="w", padx=20, pady=2)

        ctk.CTkFrame(left, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(left, text="REQUEST QUEUE (comma-sep)", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(4,2))
        self.req_entry = ctk.CTkEntry(left, width=260, font=ctk.CTkFont("Consolas",11))
        self.req_entry.insert(0, "98, 183, 37, 122, 14, 124, 65, 67")
        self.req_entry.pack(padx=16, pady=4)

        ctk.CTkLabel(left, text="INITIAL HEAD POSITION", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.head_entry = ctk.CTkEntry(left, width=260, font=ctk.CTkFont("Consolas",11))
        self.head_entry.insert(0, "53")
        self.head_entry.pack(padx=16, pady=4)

        ctk.CTkLabel(left, text="DISK SIZE", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.disk_entry = ctk.CTkEntry(left, width=260, font=ctk.CTkFont("Consolas",11))
        self.disk_entry.insert(0, "200")
        self.disk_entry.pack(padx=16, pady=4)

        ctk.CTkButton(left, text="▶ RUN", fg_color=ACCENT, text_color=BG,
                       hover_color="#00b894", font=ctk.CTkFont("Consolas",12,"bold"),
                       height=38, command=self._run).pack(fill="x", padx=16, pady=12)

        ctk.CTkButton(left, text="📊 COMPARE ALL", fg_color=ACCENT2, text_color=TEXT,
                       hover_color="#6d28d9", font=ctk.CTkFont("Consolas",11,"bold"),
                       height=34, command=self._compare).pack(fill="x", padx=16, pady=4)

        # Right
        right = ctk.CTkFrame(main, fg_color=BG)
        right.pack(side="right", fill="both", expand=True)

        self.stats_frame = ctk.CTkFrame(right, fg_color=BG)
        self.stats_frame.pack(fill="x", padx=16, pady=(12,4))

        ctk.CTkLabel(right, text="SEEK PATH VISUALIZATION", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.disk_canvas = Canvas(right, bg=CARD, height=300, highlightthickness=0)
        self.disk_canvas.pack(fill="both", expand=True, padx=16, pady=(0,4))

        self.order_label = ctk.CTkLabel(right, text="", font=ctk.CTkFont("Consolas",10),
                                         text_color=SUBTEXT, wraplength=700)
        self.order_label.pack(fill="x", padx=16, pady=(0,12))

    def _parse(self):
        try:
            reqs = [int(x.strip()) for x in self.req_entry.get().split(",")]
            head = int(self.head_entry.get())
            disk = int(self.disk_entry.get())
            return reqs, head, disk
        except:
            messagebox.showerror("Error", "Invalid input."); return None, None, None

    def _run(self):
        reqs, head, disk = self._parse()
        if reqs is None: return
        algo = self.algo_var.get()
        funcs = {
            "fcfs": lambda: disk_fcfs(reqs, head),
            "sstf": lambda: disk_sstf(reqs, head),
            "scan": lambda: disk_scan(reqs, head, disk),
            "cscan": lambda: disk_cscan(reqs, head, disk),
        }
        path, seek = funcs[algo]()
        self._draw(path, seek, disk, algo.upper())

    def _draw(self, path, seek, disk, name):
        # Stats
        for w in self.stats_frame.winfo_children(): w.destroy()
        for label, val, col in [("Total Seek", str(seek), "#f59e0b"),
                                 ("Algorithm", name, ACCENT),
                                 ("Head Moves", str(len(path)-1), "#60a5fa")]:
            card = ctk.CTkFrame(self.stats_frame, fg_color=CARD, corner_radius=8)
            card.pack(side="left", padx=(0,8))
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont("Consolas",18,"bold"),
                         text_color=col).pack(padx=14, pady=(8,0))
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont("Consolas",9),
                         text_color=SUBTEXT).pack(padx=14, pady=(0,8))

        # Draw path
        c = self.disk_canvas; c.delete("all"); c.update_idletasks()
        W = max(c.winfo_width(), 600)
        H = max(c.winfo_height(), 280)
        pad_x, pad_y = 40, 30
        n = len(path)
        max_cyl = disk

        x_scale = (W - 2*pad_x) / max(max_cyl, 1)
        y_step = (H - 2*pad_y) / max(n - 1, 1)

        # Draw axis
        c.create_line(pad_x, pad_y-10, pad_x, H-pad_y+10, fill=SUBTEXT, width=1)
        c.create_line(pad_x-10, pad_y, W-pad_x+10, pad_y, fill=BORDER, width=1)
        for t in range(0, max_cyl+1, max_cyl//5 if max_cyl >= 5 else 1):
            x = pad_x + t * x_scale
            c.create_text(x, pad_y-12, text=str(t), font=("Consolas",7), fill=SUBTEXT)

        # Draw path
        points = []
        for i, pos in enumerate(path):
            x = pad_x + pos * x_scale
            y = pad_y + i * y_step
            points.append((x, y))

        for i in range(len(points)-1):
            x0, y0 = points[i]
            x1, y1 = points[i+1]
            col = COLORS[i % len(COLORS)]
            c.create_line(x0, y0, x1, y1, fill=col, width=2, arrow="last")

        for i, (x, y) in enumerate(points):
            col = "#f59e0b" if i == 0 else ACCENT
            c.create_oval(x-4, y-4, x+4, y+4, fill=col, outline="")
            c.create_text(x+12, y, text=str(path[i]), font=("Consolas",8), fill=TEXT)

        self.order_label.configure(text=f"Path: {' → '.join(str(p) for p in path)}")

    def _compare(self):
        reqs, head, disk = self._parse()
        if reqs is None: return
        results = {}
        for name, func in [("FCFS", lambda: disk_fcfs(reqs, head)),
                            ("SSTF", lambda: disk_sstf(reqs, head)),
                            ("SCAN", lambda: disk_scan(reqs, head, disk)),
                            ("C-SCAN", lambda: disk_cscan(reqs, head, disk))]:
            path, seek = func()
            results[name] = seek

        for w in self.stats_frame.winfo_children(): w.destroy()
        best = min(results, key=results.get)
        worst = max(results, key=results.get)
        for name, seek in sorted(results.items(), key=lambda x: x[1]):
            col = "#4ade80" if name == best else "#f87171" if name == worst else SUBTEXT
            tag = " 🏆" if name == best else " ❌" if name == worst else ""
            card = ctk.CTkFrame(self.stats_frame, fg_color=CARD, corner_radius=8)
            card.pack(side="left", padx=(0,6))
            ctk.CTkLabel(card, text=str(seek), font=ctk.CTkFont("Consolas",16,"bold"),
                         text_color=col).pack(padx=10, pady=(6,0))
            ctk.CTkLabel(card, text=name+tag, font=ctk.CTkFont("Consolas",8),
                         text_color=col).pack(padx=10, pady=(0,6))

        self.order_label.configure(text=f"📊 Best: {best} (seek={results[best]}) | Worst: {worst} (seek={results[worst]})")
