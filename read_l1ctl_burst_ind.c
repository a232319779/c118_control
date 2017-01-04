#include <stdio.h>
#include <stdint.h>
#include <netinet/in.h>

#define RSL_CHAN_NR_MASK	0xf8
#define RSL_CHAN_NR_1		0x08
#define RSL_CHAN_Bm_ACCHs	0x08
#define RSL_CHAN_Lm_ACCHs	0x10
#define RSL_CHAN_SDCCH4_ACCH	0x20
#define RSL_CHAN_SDCCH8_ACCH	0x40
#define RSL_CHAN_BCCH		0x80
#define RSL_CHAN_RACH		0x88
#define RSL_CHAN_PCH_AGCH	0x90

#define BI_FLG_DUMMY    (1<<4)
#define BI_FLG_SACCH    (1<<5)
#define GSMTAP_ARFCN_F_UPLINK 0x4000

struct l1ctl_burst_ind {
	uint32_t frame_nr;
	uint16_t band_arfcn;    /* ARFCN + band + ul indicator               */
	uint8_t chan_nr;        /* GSM 08.58 channel number (9.3.1)          */
	uint8_t flags;          /* BI_FLG_xxx + burst_id = 2LSBs             */
	uint8_t rx_level;       /* 0 .. 63 in typical GSM notation (dBm+110) */
	uint8_t snr;            /* Reported SNR >> 8 (0-255)                 */
	uint8_t bits[15];       /* 114 bits + 2 steal bits. Filled MSB first */
} __attribute__((packed));

int rsl_dec_chan_nr(uint8_t chan_nr, uint8_t *type, uint8_t *subch, uint8_t *timeslot)
{
	*timeslot = chan_nr & 0x7;

	if ((chan_nr & 0xf8) == RSL_CHAN_Bm_ACCHs) {
		*type = RSL_CHAN_Bm_ACCHs;
		*subch = 0;
	} else if ((chan_nr & 0xf0) == RSL_CHAN_Lm_ACCHs) {
		*type = RSL_CHAN_Lm_ACCHs;
		*subch = (chan_nr >> 3) & 0x1;
	} else if ((chan_nr & 0xe0) == RSL_CHAN_SDCCH4_ACCH) {
		*type = RSL_CHAN_SDCCH4_ACCH;
		*subch = (chan_nr >> 3) & 0x3;
	} else if ((chan_nr & 0xc0) == RSL_CHAN_SDCCH8_ACCH) {
		*type = RSL_CHAN_SDCCH8_ACCH;
		*subch = (chan_nr >> 3) & 0x7;
	} else if (chan_nr == 0x10) {
		*type = RSL_CHAN_BCCH;
		*subch = 0;
	} else if (chan_nr == 0x11) {
		*type = RSL_CHAN_RACH;
		*subch = 0;
	} else if (chan_nr == 0x12) {
		*type = RSL_CHAN_PCH_AGCH;
		*subch = 0;
	} else
		return -1;

	return 0;
}

void print_l1ctl_burst_ind(struct l1ctl_burst_ind *bi)
{
    uint32_t fn;
    uint16_t arfcn;
    uint8_t ul, ts, flags, rx_level, snr, type, subch;

    fn = ntohl(bi->frame_nr);
    arfcn = ntohs(bi->band_arfcn);
    ul = !!(arfcn & GSMTAP_ARFCN_F_UPLINK);
    flags = bi->flags;
    rx_level = bi->rx_level;
    snr = bi->snr;
    rsl_dec_chan_nr(bi->chan_nr, &type, &subch, &ts);

    if(RSL_CHAN_Bm_ACCHs == type)
    {
	    /*
    	printf("dir:%d\nframe_nr : %u\nband_arfcn: %u\nts:%u\nflags:%u\nrx_level:%u\nsnr:%u\n",
		    ul, fn, arfcn, ts, flags, rx_level, snr);
    	printf("bit:");
    	for(int i = 0; i < 15; i++)
		printf("%02X", bi->bits[i]);
    	printf("\n");
	*/
	printf("frame_nr : %u\tts : %u\n", fn, ts);
    }
    //printf("-----------------------------------------\n");
}

int main(int argc, char *argv[])
{
    int ret = -1;
    struct l1ctl_burst_ind bi;
    
    if(argc < 2)
    {
	printf("not find file.\n");
	return 0;
    }

    FILE *fp = NULL;
    fp = fopen(argv[1], "rb");
    if(fp == NULL)
    {
	printf("open file failed.\n");
	return 0;
    }

    while(!feof(fp))
    {
	ret = fread(&bi, sizeof(bi), 1, fp);
	if(!ret)
	    break;
	print_l1ctl_burst_ind(&bi);
    }

    return 1;
}
