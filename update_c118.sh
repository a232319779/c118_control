folder="./c118"

if [ ! -x "$folder" ];then
    mkdir "$folder"
fi

cp ~/GSM/osmocombb_gprs_sniffer_real_time/src/host/osmocon/osmocon "$folder" 
cp ~/GSM/osmocombb_gprs_sniffer_real_time/src/host/layer23/src/misc/ccch_scan "$folder" 
cp ~/GSM/osmocombb_gprs_sniffer_real_time/src/target/firmware/board/compal_e88/layer1.compalram.bin "$folder"
cp ~/GSM/osmocombb_gprs_sniffer_real_time/src/host/layer23/src/misc/cell_log "$folder"
cp ~/GSM/osmocombb_gprs_sniffer_real_time/src/host/gprsdecode/gprsdecode "$folder"

