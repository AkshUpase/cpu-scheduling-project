#include <stdio.h>
#include "../include/scheduling.h"

void priority_sch(struct process p[], int n)
{
    int time = 0, completed = 0;
    int is_completed[n];

    // Initialize
    for(int i = 0; i < n; i++)
    {
        is_completed[i] = 0;
    }

    while(completed < n)
    {
        int idx = -1;
        int highest_priority = 1e9;

        for(int i = 0; i < n; i++)
        {
            // Check if process has arrived and not completed
            if(p[i].arrival <= time && is_completed[i] == 0)
            {
                // Lower value = higher priority
                if(p[i].priority < highest_priority)
                {
                    highest_priority = p[i].priority;
                    idx = i;
                }

                // Tie breaker: earlier arrival
                else if(p[i].priority == highest_priority)
                {
                    if(p[i].arrival < p[idx].arrival)
                        idx = i;
                }
            }
        }

        if(idx != -1)
        {
            // Execute completely (Non-preemptive)
            time += p[idx].burst;

            p[idx].waiting = time - p[idx].arrival - p[idx].burst;
            p[idx].turnaround = time - p[idx].arrival;

            is_completed[idx] = 1;
            completed++;
        }
        else
        {
            time++; // CPU idle
        }
    }

    display(p, n);
}