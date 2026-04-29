# 🧠 OS Simulator — Advanced Edition

A **premium, interactive Operating System Simulator** with a dark-themed GUI, covering **CPU Scheduling, Memory Management, Deadlock Handling, and Disk Scheduling** — built with Python (CustomTkinter) and C.

> **Author:** Aksh Upase (SE Engineering)

---

## 🚀 Features

### 🧠 CPU Scheduling (7 Algorithms)
| Algorithm | Type |
|---|---|
| FCFS (First Come First Served) | Non-Preemptive |
| SJF (Shortest Job First) | Non-Preemptive |
| **SRTF (Shortest Remaining Time First)** | Preemptive ⭐ |
| Round Robin | Preemptive |
| Priority Scheduling | Non-Preemptive |
| **Multilevel Queue** | Multi-Queue |
| **MLFQ (Multilevel Feedback Queue)** | Adaptive ⭐ |

### 💾 Memory Management
- **Memory Allocation:** First Fit, Best Fit, Worst Fit, **Next Fit**
- **Page Replacement:** FIFO, **LRU ⭐**, **Optimal ⭐**
- Visual block allocation + step-by-step page table

### ⚠️ Deadlock
- **Banker's Algorithm ⭐** (Deadlock Avoidance) — with step-by-step safe sequence
- **Deadlock Detection** — identifies deadlocked processes

### 💽 Disk Scheduling (6 Algorithms)
| Algorithm | Description |
|---|---|
| FCFS | Order of arrival |
| SSTF | Nearest request first |
| **SCAN (Elevator)** | Sweep + reverse |
| **C-SCAN** | Circular sweep |
| **LOOK** | SCAN without going to edges |
| **C-LOOK** | C-SCAN without going to edges |

### 🎨 Premium UI Features
- 🌙 **Dark Mode** with custom color palette
- 📊 **Comparison Mode** — compare all CPU algorithms side-by-side
- 📈 **Gantt Charts** & **Seek Path Visualizations**
- 🏆 **Auto-Analysis** — recommends best/worst algorithm
- 🎲 **Random Test Case Generator**
- 💾 **Export to CSV**
- 📚 **Theory/Learn Section** — explains every algorithm with pros/cons

---

## 🏗️ Project Structure

```
cpu-scheduling-project/
├── src/                    # C backend (original)
│   ├── main.c
│   ├── fcfs.c
│   ├── SJF.c
│   ├── round_robin.c
│   ├── priority_sch.c
│   └── input.c
├── include/
│   └── scheduling.h
├── ui/                     # Python GUI (upgraded)
│   ├── app.py              # ⭐ Main entry point
│   ├── algorithms.py       # All algorithm implementations
│   └── tabs/
│       ├── cpu_tab.py      # CPU Scheduling tab
│       ├── memory_tab.py   # Memory Management tab
│       ├── deadlock_tab.py # Deadlock tab
│       ├── disk_tab.py     # Disk Scheduling tab
│       ├── compare_tab.py  # Algorithm Comparison tab
│       └── learn_tab.py    # Theory/Learn tab
├── output/
├── docs/
└── scheduler.exe
```

---

## ⚙️ How to Run

### Prerequisites
```bash
pip install customtkinter matplotlib
```

### Launch the App
```bash
cd cpu-scheduling-project/ui
python app.py
```

### Compile C Backend (Optional)
```bash
gcc src/main.c src/fcfs.c src/input.c src/SJF.c src/round_robin.c src/priority_sch.c -o scheduler
```

---

## 📸 Tabs Overview

| Tab | What It Does |
|---|---|
| 🧠 CPU Scheduling | Run any of 7 algorithms with Gantt chart |
| 💾 Memory | Memory allocation + Page replacement simulation |
| ⚠️ Deadlock | Banker's Algorithm + Deadlock Detection |
| 💽 Disk Scheduling | 6 algorithms with seek path visualization |
| 📊 Compare All | Compare all CPU algorithms on same data |
| 📚 Learn | Theory section with pros/cons of each algorithm |

---

## 📄 License

Open-source for educational purposes.

⭐ If you found this project useful, consider giving it a star!
