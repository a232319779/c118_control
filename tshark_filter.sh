#!/bin/bash

for arg in "$@"
do
    echo process $arg file ...
    echo modify $arg file to non root ...
    sudo chown newsun:newsun $arg
    tshark -r $arg -Y 'gsm_rlcmac.dl_payload_type==0' -T fields -e gsm_rlcmac.dl.tfi -e gsm_rlcmac.bsn -e data > $arg.txt
    echo process ok
done
