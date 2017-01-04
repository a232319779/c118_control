compile:
	gcc -std=c99 -g -o read_burst_ind read_l1ctl_burst_ind.c 
	gcc -std=c99 -g -o test_pipe_r test_pipe_r.c 
	gcc -std=c99 -g -o test_pipe test_pipe.c 

.PHONY : clean
clean :
	rm read_burst_ind test_pipe_r test_pipe 
