"""Memory Management Tab — Allocation + Page Replacement with visualization."""
import customtkinter as ctk
from tkinter import Canvas, messagebox
import random, csv, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms import (first_fit, best_fit, worst_fit, next_fit,
                         fifo_page_replacement, lru_page_replacement, optimal_page_replacement)

ACCENT="#00d4aa"; ACCENT2="#7c3aed"; BG="#0d1117"; PANEL="#161b22"
CARD="#1c2230"; BORDER="#30363d"; TEXT="#e6edf3"; SUBTEXT="#8b949e"
COLORS=["#00d4aa","#7c3aed","#f59e0b","#f87171","#4ade80","#60a5fa","#f472b6","#fb923c"]

class MemoryTab:
    def __init__(self, parent):
        self.parent = parent
        self._build()

    def _build(self):
        main = ctk.CTkFrame(self.parent, fg_color=BG)
        main.pack(fill="both", expand=True)

        # Sub-tabs for allocation vs page replacement
        sub = ctk.CTkTabview(main, fg_color=BG, segmented_button_fg_color=PANEL,
                              segmented_button_selected_color=ACCENT2,
                              segmented_button_selected_hover_color="#6d28d9")
        sub.pack(fill="both", expand=True, padx=8, pady=4)
        sub.add("📦 Memory Allocation")
        sub.add("📄 Page Replacement")
        self._build_alloc(sub.tab("📦 Memory Allocation"))
        self._build_paging(sub.tab("📄 Page Replacement"))

    # ═══ ALLOCATION ═══════════════════════════════════════════════════════════
    def _build_alloc(self, parent):
        left = ctk.CTkFrame(parent, fg_color=PANEL, width=300, corner_radius=0)
        left.pack(side="left", fill="y"); left.pack_propagate(False)

        ctk.CTkLabel(left, text="ALGORITHM", font=ctk.CTkFont("Consolas",11,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(12,4))
        self.alloc_algo = ctk.StringVar(value="first")
        for label, val in [("First Fit","first"),("Best Fit","best"),("Worst Fit","worst"),("Next Fit","next")]:
            ctk.CTkRadioButton(left, text=label, variable=self.alloc_algo, value=val,
                               font=ctk.CTkFont("Consolas",11), text_color=TEXT,
                               fg_color=ACCENT, hover_color=ACCENT2).pack(anchor="w", padx=20, pady=2)

        ctk.CTkFrame(left, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(left, text="MEMORY BLOCKS (comma-sep)", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(4,2))
        self.blocks_entry = ctk.CTkEntry(left, font=ctk.CTkFont("Consolas",11), width=260)
        self.blocks_entry.insert(0, "100, 500, 200, 300, 600")
        self.blocks_entry.pack(padx=16, pady=4)

        ctk.CTkLabel(left, text="PROCESS SIZES (comma-sep)", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.psizes_entry = ctk.CTkEntry(left, font=ctk.CTkFont("Consolas",11), width=260)
        self.psizes_entry.insert(0, "212, 417, 112, 426")
        self.psizes_entry.pack(padx=16, pady=4)

        ctk.CTkButton(left, text="▶ ALLOCATE", fg_color=ACCENT, text_color=BG,
                       hover_color="#00b894", font=ctk.CTkFont("Consolas",12,"bold"),
                       height=38, command=self._run_alloc).pack(fill="x", padx=16, pady=12)

        # Right
        right = ctk.CTkFrame(parent, fg_color=BG)
        right.pack(side="right", fill="both", expand=True)
        self.alloc_canvas = Canvas(right, bg=CARD, height=180, highlightthickness=0)
        self.alloc_canvas.pack(fill="x", padx=16, pady=(12,4))
        self.alloc_table = ctk.CTkScrollableFrame(right, fg_color=CARD, height=250)
        self.alloc_table.pack(fill="both", expand=True, padx=16, pady=(4,12))

    def _run_alloc(self):
        try:
            blocks = [int(x.strip()) for x in self.blocks_entry.get().split(",")]
            psizes = [int(x.strip()) for x in self.psizes_entry.get().split(",")]
        except:
            messagebox.showerror("Error", "Enter comma-separated integers."); return

        funcs = {"first": first_fit, "best": best_fit, "worst": worst_fit, "next": next_fit}
        alloc, remaining = funcs[self.alloc_algo.get()](blocks, psizes)

        # Draw blocks visualization
        c = self.alloc_canvas; c.delete("all"); c.update_idletasks()
        W = max(c.winfo_width(), 500)
        total = sum(blocks)
        x = 10
        for i, b in enumerate(blocks):
            w = max(30, (b / total) * (W - 20))
            c.create_rectangle(x, 20, x+w, 80, fill=COLORS[i%len(COLORS)], outline=CARD)
            c.create_text(x+w/2, 40, text=f"B{i+1}", font=("Consolas",9,"bold"), fill=BG)
            c.create_text(x+w/2, 60, text=f"{b}KB", font=("Consolas",8), fill=BG)
            c.create_text(x+w/2, 95, text=f"Rem:{remaining[i]}", font=("Consolas",8), fill=SUBTEXT)
            x += w + 2

        # Table
        for w in self.alloc_table.winfo_children(): w.destroy()
        hdr = ctk.CTkFrame(self.alloc_table, fg_color=PANEL)
        hdr.pack(fill="x", pady=(0,4))
        for col in ["Process","Size","Block","Block Size","Status"]:
            ctk.CTkLabel(hdr, text=col, font=ctk.CTkFont("Consolas",10,"bold"),
                         text_color=ACCENT, width=100).pack(side="left", padx=4)
        for i, (ps, bi, bs) in enumerate(alloc):
            row = ctk.CTkFrame(self.alloc_table, fg_color=CARD)
            row.pack(fill="x", pady=1)
            status = f"✅ Block {bi+1}" if bi != -1 else "❌ Not Allocated"
            col = "#4ade80" if bi != -1 else "#f87171"
            for val in [f"P{i+1}", f"{ps}KB", f"B{bi+1}" if bi!=-1 else "—", f"{bs}KB" if bi!=-1 else "—", status]:
                ctk.CTkLabel(row, text=str(val), font=ctk.CTkFont("Consolas",10),
                             text_color=col, width=100).pack(side="left", padx=4)

    # ═══ PAGE REPLACEMENT ═════════════════════════════════════════════════════
    def _build_paging(self, parent):
        left = ctk.CTkFrame(parent, fg_color=PANEL, width=300, corner_radius=0)
        left.pack(side="left", fill="y"); left.pack_propagate(False)

        ctk.CTkLabel(left, text="ALGORITHM", font=ctk.CTkFont("Consolas",11,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(12,4))
        self.page_algo = ctk.StringVar(value="fifo")
        for label, val in [("FIFO","fifo"),("LRU ⭐","lru"),("Optimal ⭐","optimal")]:
            ctk.CTkRadioButton(left, text=label, variable=self.page_algo, value=val,
                               font=ctk.CTkFont("Consolas",11), text_color=TEXT,
                               fg_color=ACCENT, hover_color=ACCENT2).pack(anchor="w", padx=20, pady=2)

        ctk.CTkFrame(left, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=8)
        ctk.CTkLabel(left, text="PAGE REF STRING (comma-sep)", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(4,2))
        self.pages_entry = ctk.CTkEntry(left, font=ctk.CTkFont("Consolas",11), width=260)
        self.pages_entry.insert(0, "7,0,1,2,0,3,0,4,2,3,0,3,2")
        self.pages_entry.pack(padx=16, pady=4)

        ctk.CTkLabel(left, text="FRAMES", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.frames_entry = ctk.CTkEntry(left, font=ctk.CTkFont("Consolas",11), width=260)
        self.frames_entry.insert(0, "3")
        self.frames_entry.pack(padx=16, pady=4)

        ctk.CTkButton(left, text="▶ SIMULATE", fg_color=ACCENT, text_color=BG,
                       hover_color="#00b894", font=ctk.CTkFont("Consolas",12,"bold"),
                       height=38, command=self._run_paging).pack(fill="x", padx=16, pady=12)

        right = ctk.CTkFrame(parent, fg_color=BG)
        right.pack(side="right", fill="both", expand=True)
        self.page_stats = ctk.CTkFrame(right, fg_color=BG)
        self.page_stats.pack(fill="x", padx=16, pady=(12,4))
        self.page_table = ctk.CTkScrollableFrame(right, fg_color=CARD, height=400)
        self.page_table.pack(fill="both", expand=True, padx=16, pady=(4,12))

    def _run_paging(self):
        try:
            pages = [int(x.strip()) for x in self.pages_entry.get().split(",")]
            frames = int(self.frames_entry.get())
            assert frames > 0
        except:
            messagebox.showerror("Error", "Invalid input."); return

        funcs = {"fifo": fifo_page_replacement, "lru": lru_page_replacement, "optimal": optimal_page_replacement}
        history, faults, hits = funcs[self.page_algo.get()](pages, frames)

        # Stats
        for w in self.page_stats.winfo_children(): w.destroy()
        ratio = hits / len(pages) * 100 if pages else 0
        for label, val, col in [("Page Faults", str(faults), "#f87171"),
                                 ("Page Hits", str(hits), "#4ade80"),
                                 ("Hit Ratio", f"{ratio:.1f}%", "#60a5fa")]:
            card = ctk.CTkFrame(self.page_stats, fg_color=CARD, corner_radius=8)
            card.pack(side="left", padx=(0,8))
            ctk.CTkLabel(card, text=val, font=ctk.CTkFont("Consolas",20,"bold"),
                         text_color=col).pack(padx=14, pady=(8,0))
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont("Consolas",9),
                         text_color=SUBTEXT).pack(padx=14, pady=(0,8))

        # Table
        for w in self.page_table.winfo_children(): w.destroy()
        hdr = ctk.CTkFrame(self.page_table, fg_color=PANEL)
        hdr.pack(fill="x", pady=(0,4))
        for col in ["Step", "Page", "Frames", "Status"]:
            ctk.CTkLabel(hdr, text=col, font=ctk.CTkFont("Consolas",10,"bold"),
                         text_color=ACCENT, width=120).pack(side="left", padx=4)
        for i, (page, frame_state, is_fault) in enumerate(history):
            row = ctk.CTkFrame(self.page_table, fg_color=CARD)
            row.pack(fill="x", pady=1)
            status = "❌ FAULT" if is_fault else "✅ HIT"
            col = "#f87171" if is_fault else "#4ade80"
            frames_str = " | ".join(str(f) for f in frame_state)
            for val in [i+1, page, frames_str, status]:
                ctk.CTkLabel(row, text=str(val), font=ctk.CTkFont("Consolas",10),
                             text_color=col, width=120).pack(side="left", padx=4)
