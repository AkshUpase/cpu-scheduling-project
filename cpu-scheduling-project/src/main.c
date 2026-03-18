#include<stdio.h>
#include "../include/scheduling.h"

int main()
{
    int n;

    printf("Enter number of processes: ");
    scanf("%d",&n);

    struct process p[n];

    input(p,n);

    printf("\nRunning FCFS Scheduling...\n");

    fcfs(p,n);

    return 0;
}