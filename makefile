CC=gcc
CFLAGS=-I.

life: life.c lifefunc.c
	$(CC) -o life life.c lifefunc.c $(CFLAGS)
