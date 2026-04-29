#include <stdio.h>
#include <string.h>
#include "../include/scheduling.h"

int main(int argc, char *argv[])
{
    int n;

    if (argc < 2) {
        printf("Usage: scheduler.exe <ALGORITHM>\n");
        return 1;
    }

    printf("Enter number of processes: ");
    scanf("%d", &n);

    struct process p[n];

    input(p, n);

    printf("\nRunning %s Scheduling...\n", argv[1]);

    if (strcmp(argv[1], "FCFS") == 0) {
        fcfs(p, n);
    }
    else if (strcmp(argv[1], "SJF") == 0) {
        sjf(p, n);
    }
    else if (strcmp(argv[1], "Round") == 0) {
        int quantum;
        printf("Enter Time Quantum: ");
        scanf("%d", &quantum);

        round_robin(p, n, quantum);
    }
    else if (strcmp(argv[1], "Priority") == 0) {
        priority_scheduling(p, n);
    }
    else {
        printf("Invalid Algorithm!\n");
    }

    return 0;
}