#include<stdio.h>
#include "../include/scheduling.h"

void fcfs(struct process p[], int n)
{
    int time=0;

    for(int i=0;i<n;i++)
    {
        if(time < p[i].arrival)
            time = p[i].arrival;

        p[i].waiting = time - p[i].arrival;

        time += p[i].burst;

        p[i].turnaround = p[i].waiting + p[i].burst;
    }

    display(p,n);
}