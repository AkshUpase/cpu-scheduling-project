#ifndef SCHEDULING_H
#define SCHEDULING_H

struct process
{
    int pid;
    int arrival;
    int burst;
    int waiting;
    int turnaround;
};

void input(struct process p[], int n);
void display(struct process p[], int n);
void fcfs(struct process p[], int n);
void sjf(struct process[], int n);
void round_robin(struct process p[], int n, int quantum);

#endif