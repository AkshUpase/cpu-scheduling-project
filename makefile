all:
	gcc src/main.c src/fcfs.c src/input.c -o scheduler

run:
	./scheduler