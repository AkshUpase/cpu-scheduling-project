#include <stdio.h>
#include "../include/scheduling.h"

void round_robin(struct process p[], int n, int quantum)
{
    int time = 0, completed = 0;
    int rem_bt[n];       // remaining burst time
    int is_completed[n];

    // Initialize
    for(int i = 0; i < n; i++)
    {
        rem_bt[i] = p[i].burst;
        is_completed[i] = 0;
    }

    while(completed < n)
    {
        int done = 1;

        for(int i = 0; i < n; i++)
        {
            if(p[i].arrival <= time && rem_bt[i] > 0)
            {
                done = 0;

                // If remaining burst > quantum
                if(rem_bt[i] > quantum)
                {
                    time += quantum;
                    rem_bt[i] -= quantum;
                }
                else
                {
                    // Last execution
                    time += rem_bt[i];

                    p[i].waiting = time - p[i].arrival - p[i].burst;
                    p[i].turnaround = time - p[i].arrival;

                    rem_bt[i] = 0;
                    is_completed[i] = 1;
                    completed++;
                }
            }
        }

        // If no process executed, increment time
        if(done)
            time++;
    }

    display(p, n);
}