#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>

#include "burst_desc.h"

int main(int argc, char *argv[])
{
    int pipe_wd = -1;
    FILE *fp = NULL;

    struct l1ctl_burst_ind bi = {0};


    //fp = fopen(argv[1], "rb");
    fp = fopen("bursts_20161128_2048_576_764981_0f.dat", "rb");
    pipe_wd = open("/tmp/gprs_fifo", O_WRONLY);

    int count = 0;
    while(!feof(fp))
    {
	fread(&bi, sizeof(bi), 1, fp);
	write(pipe_wd, &bi, sizeof(bi));
	
	printf("bi : %u\tcount : %d\n", bi.frame_nr, count++);
    }
    close(pipe_wd);
    fclose(fp);

    return 0;
}
