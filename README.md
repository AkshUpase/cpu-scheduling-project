# 🧠 CPU Scheduling Simulator (FCFS)

A simple and interactive **CPU Scheduling Simulator** implemented in **C** (with optional Python UI), designed to demonstrate core **Operating System scheduling concepts** such as **First Come First Serve (FCFS)**.

---

## 📌 Project Overview

This project simulates how an operating system schedules processes using the **FCFS (First Come First Serve)** algorithm. It takes user input for processes and calculates:

* Waiting Time (WT)
* Turnaround Time (TAT)
* Average Waiting Time
* Average Turnaround Time

---

## 🚀 Features

* 📥 User input for multiple processes
* ⏱️ FCFS Scheduling implementation
* 📊 Displays process table with:

  * Process ID
  * Arrival Time
  * Burst Time
  * Waiting Time
  * Turnaround Time
* 📈 Calculates average performance metrics
* 🖥️ Optional Python-based UI included

---

## 🏗️ Project Structure

```
cpu-scheduling-project/
│
├── src/
│   ├── main.c          # Entry point of program
│   ├── fcfs.c          # FCFS scheduling logic
│   └── input.c         # Input & display functions
│
├── include/
│   └── scheduling.h    # Structure & function declarations
│
├── docs/
│   └── methodology.txt # Project explanation
│
├── output/
│   └── sample_output.txt
│
├── ui/
│   ├── ui.py           # Python UI (optional)
│   └── ui1.py
│
├── scheduler.exe       # Compiled executable
└── makefile            # Build automation
```

---

## ⚙️ How It Works

1. User enters number of processes
2. Inputs arrival time and burst time
3. FCFS algorithm schedules processes in order of arrival
4. System computes:

   * Waiting Time = Start Time − Arrival Time
   * Turnaround Time = Waiting Time + Burst Time
5. Final table and averages are displayed

---

## 🧮 Algorithm Used

### First Come First Serve (FCFS)

* Processes are executed in the order they arrive
* Non-preemptive scheduling
* Simple but may cause **long waiting times**

---

## 🛠️ Installation & Usage

### 🔧 Compile (Linux / Mac / MinGW)

```bash
gcc src/main.c src/fcfs.c src/input.c -o scheduler
```

### ▶️ Run

```bash
./scheduler
```

### 🪟 Windows (Executable)

You can directly run:

```
scheduler.exe
```

---

## 💻 Sample Output

```
PID    AT    BT    WT    TAT
1      0     5     0     5
2      1     3     4     7
3      2     8     6     14

Average Waiting Time = 3.33
Average Turnaround Time = 8.67
```

---

## 📚 Learning Outcomes

* Understanding of CPU Scheduling Algorithms
* Practical implementation of FCFS
* Calculation of scheduling metrics
* Modular C programming structure

---

## 🔮 Future Enhancements

* Add more algorithms:

  * 🔁 Round Robin
  * ⚡ Shortest Job First (SJF)
  * 🎯 Priority Scheduling
* Gantt Chart visualization
* Full GUI integration
* Real-time simulation

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo and submit a pull request.

---

## 📄 License

This project is open-source and free to use for educational purposes.

---

## 👨‍💻 Author

**Aksh Upase**
(Second Year Engineering Student)

---

⭐ If you found this project useful, consider giving it a star!
