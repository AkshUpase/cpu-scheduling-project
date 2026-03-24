#include <stdio.h>
#include "../include/scheduling.h"

void sjf(struct process p[], int n)
{
    int time = 0, completed = 0;
    int is_completed[n];

    for(int i = 0; i < n; i++)
        is_completed[i] = 0;

    while(completed < n)
    {
        int idx = -1;
        int min_burst = 1e9;

        // Find process with minimum burst time among arrived processes
        for(int i = 0; i < n; i++)
        {
            if(p[i].arrival <= time && is_completed[i] == 0)
            {
                if(p[i].burst < min_burst)
                {
                    min_burst = p[i].burst;
                    idx = i;
                }
            }
        }

        // If no process is found, increment time
        if(idx == -1)
        {
            time++;
        }
        else
        {
            p[idx].waiting = time - p[idx].arrival;
            time += p[idx].burst;
            p[idx].turnaround = p[idx].waiting + p[idx].burst;

            is_completed[idx] = 1;
            completed++;
        }
    }

    display(p, n);
}