#!/bin/bash

for arg in "$@"
do
    echo process $arg
    text2pcap -l 169 $arg $arg.pcap
done
