"""Deadlock Tab — Banker's Algorithm + Deadlock Detection."""
import customtkinter as ctk
from tkinter import messagebox
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from algorithms import bankers_algorithm, deadlock_detection

ACCENT="#00d4aa"; ACCENT2="#7c3aed"; BG="#0d1117"; PANEL="#161b22"
CARD="#1c2230"; BORDER="#30363d"; TEXT="#e6edf3"; SUBTEXT="#8b949e"

class DeadlockTab:
    def __init__(self, parent):
        self.parent = parent
        self._build()

    def _build(self):
        main = ctk.CTkFrame(self.parent, fg_color=BG)
        main.pack(fill="both", expand=True)

        sub = ctk.CTkTabview(main, fg_color=BG, segmented_button_fg_color=PANEL,
                              segmented_button_selected_color=ACCENT2)
        sub.pack(fill="both", expand=True, padx=8, pady=4)
        sub.add("🏦 Banker's Algorithm")
        sub.add("🔍 Deadlock Detection")
        self._build_bankers(sub.tab("🏦 Banker's Algorithm"))
        self._build_detection(sub.tab("🔍 Deadlock Detection"))

    def _build_bankers(self, parent):
        left = ctk.CTkFrame(parent, fg_color=PANEL, width=340, corner_radius=0)
        left.pack(side="left", fill="y"); left.pack_propagate(False)

        ctk.CTkLabel(left, text="BANKER'S ALGORITHM ⭐", font=ctk.CTkFont("Consolas",12,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(12,4))
        ctk.CTkLabel(left, text="Deadlock Avoidance", font=ctk.CTkFont("Consolas",10),
                     text_color=SUBTEXT).pack(anchor="w", padx=16)

        ctk.CTkFrame(left, fg_color=BORDER, height=1).pack(fill="x", padx=16, pady=8)

        ctk.CTkLabel(left, text="Processes / Resources", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(4,2))
        r1 = ctk.CTkFrame(left, fg_color=PANEL)
        r1.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(r1, text="P:", font=ctk.CTkFont("Consolas",10), text_color=SUBTEXT).pack(side="left")
        self.bn_p = ctk.CTkEntry(r1, width=40, font=ctk.CTkFont("Consolas",10))
        self.bn_p.insert(0, "5"); self.bn_p.pack(side="left", padx=4)
        ctk.CTkLabel(r1, text="R:", font=ctk.CTkFont("Consolas",10), text_color=SUBTEXT).pack(side="left", padx=(8,0))
        self.bn_r = ctk.CTkEntry(r1, width=40, font=ctk.CTkFont("Consolas",10))
        self.bn_r.insert(0, "3"); self.bn_r.pack(side="left", padx=4)

        ctk.CTkLabel(left, text="Available (comma-sep)", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.bn_avail = ctk.CTkEntry(left, width=280, font=ctk.CTkFont("Consolas",10))
        self.bn_avail.insert(0, "3, 3, 2"); self.bn_avail.pack(padx=16, pady=2)

        ctk.CTkLabel(left, text="Max Matrix (row per line, comma-sep)", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.bn_max = ctk.CTkTextbox(left, width=280, height=80, font=ctk.CTkFont("Consolas",10))
        self.bn_max.insert("1.0", "7,5,3\n3,2,2\n9,0,2\n2,2,2\n4,3,3")
        self.bn_max.pack(padx=16, pady=2)

        ctk.CTkLabel(left, text="Allocation Matrix (row per line)", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.bn_alloc = ctk.CTkTextbox(left, width=280, height=80, font=ctk.CTkFont("Consolas",10))
        self.bn_alloc.insert("1.0", "0,1,0\n2,0,0\n3,0,2\n2,1,1\n0,0,2")
        self.bn_alloc.pack(padx=16, pady=2)

        ctk.CTkButton(left, text="▶ CHECK SAFETY", fg_color=ACCENT, text_color=BG,
                       hover_color="#00b894", font=ctk.CTkFont("Consolas",12,"bold"),
                       height=38, command=self._run_bankers).pack(fill="x", padx=16, pady=12)

        right = ctk.CTkFrame(parent, fg_color=BG)
        right.pack(side="right", fill="both", expand=True)
        self.bn_result = ctk.CTkScrollableFrame(right, fg_color=CARD)
        self.bn_result.pack(fill="both", expand=True, padx=16, pady=12)

    def _run_bankers(self):
        try:
            avail = [int(x.strip()) for x in self.bn_avail.get().split(",")]
            max_m = [[int(x.strip()) for x in line.split(",")] for line in self.bn_max.get("1.0","end").strip().split("\n")]
            alloc_m = [[int(x.strip()) for x in line.split(",")] for line in self.bn_alloc.get("1.0","end").strip().split("\n")]
        except:
            messagebox.showerror("Error", "Invalid matrix input."); return

        is_safe, seq, steps = bankers_algorithm(avail, max_m, alloc_m)

        for w in self.bn_result.winfo_children(): w.destroy()

        # Status banner
        if is_safe:
            ctk.CTkLabel(self.bn_result, text="✅ SYSTEM IS IN SAFE STATE",
                         font=ctk.CTkFont("Consolas",16,"bold"), text_color="#4ade80").pack(pady=(12,4))
            seq_str = " → ".join([f"P{s}" for s in seq])
            ctk.CTkLabel(self.bn_result, text=f"Safe Sequence: {seq_str}",
                         font=ctk.CTkFont("Consolas",12), text_color=ACCENT).pack(pady=(0,12))
        else:
            ctk.CTkLabel(self.bn_result, text="❌ SYSTEM IS NOT SAFE — DEADLOCK POSSIBLE",
                         font=ctk.CTkFont("Consolas",16,"bold"), text_color="#f87171").pack(pady=12)

        # Step-by-step
        ctk.CTkLabel(self.bn_result, text="STEP-BY-STEP EXECUTION",
                     font=ctk.CTkFont("Consolas",11,"bold"), text_color=ACCENT).pack(anchor="w", padx=8, pady=(8,4))

        for i, step in enumerate(steps):
            frame = ctk.CTkFrame(self.bn_result, fg_color=PANEL, corner_radius=6)
            frame.pack(fill="x", padx=8, pady=2)
            ctk.CTkLabel(frame, text=f"Step {i+1}: Execute P{step['process']}",
                         font=ctk.CTkFont("Consolas",10,"bold"), text_color="#f59e0b").pack(anchor="w", padx=8, pady=(4,0))
            ctk.CTkLabel(frame, text=f"  Need: {step['need']}  |  Alloc: {step['alloc']}",
                         font=ctk.CTkFont("Consolas",9), text_color=SUBTEXT).pack(anchor="w", padx=8)
            ctk.CTkLabel(frame, text=f"  Work: {step['work_before']} → {step['work_after']}",
                         font=ctk.CTkFont("Consolas",9), text_color="#60a5fa").pack(anchor="w", padx=8, pady=(0,4))

    def _build_detection(self, parent):
        left = ctk.CTkFrame(parent, fg_color=PANEL, width=340, corner_radius=0)
        left.pack(side="left", fill="y"); left.pack_propagate(False)

        ctk.CTkLabel(left, text="DEADLOCK DETECTION", font=ctk.CTkFont("Consolas",12,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(12,4))

        ctk.CTkLabel(left, text="Available (comma-sep)", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(12,2))
        self.dd_avail = ctk.CTkEntry(left, width=280, font=ctk.CTkFont("Consolas",10))
        self.dd_avail.insert(0, "0, 0, 0"); self.dd_avail.pack(padx=16, pady=2)

        ctk.CTkLabel(left, text="Allocation Matrix", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.dd_alloc = ctk.CTkTextbox(left, width=280, height=80, font=ctk.CTkFont("Consolas",10))
        self.dd_alloc.insert("1.0", "0,1,0\n2,0,0\n3,0,3\n2,1,1\n0,0,2")
        self.dd_alloc.pack(padx=16, pady=2)

        ctk.CTkLabel(left, text="Request Matrix", font=ctk.CTkFont("Consolas",10,"bold"),
                     text_color=ACCENT).pack(anchor="w", padx=16, pady=(8,2))
        self.dd_req = ctk.CTkTextbox(left, width=280, height=80, font=ctk.CTkFont("Consolas",10))
        self.dd_req.insert("1.0", "0,0,0\n2,0,2\n0,0,0\n1,0,0\n0,0,2")
        self.dd_req.pack(padx=16, pady=2)

        ctk.CTkButton(left, text="▶ DETECT", fg_color="#f87171", text_color=BG,
                       hover_color="#ef4444", font=ctk.CTkFont("Consolas",12,"bold"),
                       height=38, command=self._run_detection).pack(fill="x", padx=16, pady=12)

        right = ctk.CTkFrame(parent, fg_color=BG)
        right.pack(side="right", fill="both", expand=True)
        self.dd_result = ctk.CTkScrollableFrame(right, fg_color=CARD)
        self.dd_result.pack(fill="both", expand=True, padx=16, pady=12)

    def _run_detection(self):
        try:
            avail = [int(x.strip()) for x in self.dd_avail.get().split(",")]
            alloc_m = [[int(x.strip()) for x in line.split(",")] for line in self.dd_alloc.get("1.0","end").strip().split("\n")]
            req_m = [[int(x.strip()) for x in line.split(",")] for line in self.dd_req.get("1.0","end").strip().split("\n")]
        except:
            messagebox.showerror("Error", "Invalid input."); return

        is_dead, deadlocked, safe_seq = deadlock_detection(avail, alloc_m, req_m)

        for w in self.dd_result.winfo_children(): w.destroy()

        if is_dead:
            ctk.CTkLabel(self.dd_result, text="🔴 DEADLOCK DETECTED!",
                         font=ctk.CTkFont("Consolas",16,"bold"), text_color="#f87171").pack(pady=12)
            dl_str = ", ".join([f"P{d}" for d in deadlocked])
            ctk.CTkLabel(self.dd_result, text=f"Deadlocked Processes: {dl_str}",
                         font=ctk.CTkFont("Consolas",12), text_color="#f59e0b").pack(pady=4)
        else:
            ctk.CTkLabel(self.dd_result, text="✅ NO DEADLOCK — System is safe",
                         font=ctk.CTkFont("Consolas",16,"bold"), text_color="#4ade80").pack(pady=12)
            seq_str = " → ".join([f"P{s}" for s in safe_seq])
            ctk.CTkLabel(self.dd_result, text=f"Execution Order: {seq_str}",
                         font=ctk.CTkFont("Consolas",12), text_color=ACCENT).pack(pady=4)
