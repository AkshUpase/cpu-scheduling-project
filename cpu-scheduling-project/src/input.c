#include<stdio.h>
#include "../include/scheduling.h"

void input(struct process p[], int n)
{
    for(int i=0;i<n;i++)
    {
        p[i].pid = i+1;

        printf("\nProcess %d\n",i+1);

        printf("Arrival Time: ");
        scanf("%d",&p[i].arrival);

        printf("Burst Time: ");
        scanf("%d",&p[i].burst);
    }
}

void display(struct process p[], int n)
{
    float avg_wt=0, avg_tat=0;

    printf("\nPID\tAT\tBT\tWT\tTAT\n");

    for(int i=0;i<n;i++)
    {
        printf("%d\t%d\t%d\t%d\t%d\n",
        p[i].pid,
        p[i].arrival,
        p[i].burst,
        p[i].waiting,
        p[i].turnaround);

        avg_wt += p[i].waiting;
        avg_tat += p[i].turnaround;
    }

    printf("\nAverage Waiting Time = %.2f",avg_wt/n);
    printf("\nAverage Turnaround Time = %.2f\n",avg_tat/n);
}