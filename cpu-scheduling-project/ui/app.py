"""
OS Simulator — Premium UI with customtkinter
Main application entry point with tabbed interface.
"""
import customtkinter as ctk 
from tabs.cpu_tab import CPUTab
from tabs.memory_tab import MemoryTab
from tabs.deadlock_tab import DeadlockTab
from tabs.disk_tab import DiskTab
from tabs.learn_tab import LearnTab
from tabs.compare_tab import CompareTab

# ── Theme ──────────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#00d4aa"
BG = "#0d1117"
PANEL = "#161b22"

class OSSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🧠 OS Simulator — Advanced Edition")
        self.geometry("1280x820")
        self.configure(fg_color=BG)
        self.minsize(1100, 700)
        self._build_ui()

    def _build_ui(self):
        # ── Header ──
        header = ctk.CTkFrame(self, fg_color=PANEL, height=60, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="⚙  OS SIMULATOR — ADVANCED EDITION",
                     font=ctk.CTkFont("Consolas", 20, "bold"),
                     text_color=ACCENT).pack(side="left", padx=24, pady=12)
        ctk.CTkLabel(header, text="by Group-9",
                     font=ctk.CTkFont("Consolas", 11),
                     text_color="#8b949e").pack(side="right", padx=24)

        # Accent line
        ctk.CTkFrame(self, fg_color=ACCENT, height=2, corner_radius=0).pack(fill="x")

        # ── Tabview ──
        self.tabview = ctk.CTkTabview(self, fg_color=BG,
                                       segmented_button_fg_color=PANEL,
                                       segmented_button_selected_color=ACCENT,
                                       segmented_button_selected_hover_color="#00b894",
                                       segmented_button_unselected_color=PANEL,
                                       segmented_button_unselected_hover_color="#1c2230",
                                       corner_radius=8)
        self.tabview.pack(fill="both", expand=True, padx=12, pady=(8, 12))

        tabs = ["🧠 CPU Scheduling", "💾 Memory", "⚠️ Deadlock",
                "💽 Disk Scheduling", "📊 Compare All", "📚 Learn"]
        for t in tabs:
            self.tabview.add(t)

        CPUTab(self.tabview.tab("🧠 CPU Scheduling"))
        MemoryTab(self.tabview.tab("💾 Memory"))
        DeadlockTab(self.tabview.tab("⚠️ Deadlock"))
        DiskTab(self.tabview.tab("💽 Disk Scheduling"))
        CompareTab(self.tabview.tab("📊 Compare All"))
        LearnTab(self.tabview.tab("📚 Learn"))


if __name__ == "__main__":
    app = OSSimulatorApp()
    app.mainloop()
