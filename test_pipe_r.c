#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>

#include "burst_desc.h"

int main(int argc, char *argv[])
{
    int pipe_rd = -1;
    struct l1ctl_burst_ind bi = {0};


    //fp = fopen(argv[1], "rb");
    pipe_rd = open("/tmp/gprs_fifo", O_RDONLY);

    int count = 0;
    int read_count = -1;
    
    do
    {
	read_count = read(pipe_rd, &bi, sizeof(bi));
	
	//printf("bi : %u\tcount : %d\n", bi.frame_nr, count);
	printf("bi : %u\tcount : %d\n", bi.frame_nr, count++);
    }while(read_count > 0);
    close(pipe_rd);

    return 0;
}
