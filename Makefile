all: main

main: push.c
	gcc push.c -o main

clean:
	rm -f main
