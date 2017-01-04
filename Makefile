compile:
	gcc -std=c99 -o read_burst_ind read_l1ctl_burst_ind.c 

.PHONY : clean
clean :
	rm read_burst_ind 
