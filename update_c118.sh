bin_path=./c118
osmocombb_path=~/GSM/GPRS-real-time-sniffer

if [ ! -x $bin_path ];then
    mkdir $bin_path
fi

cp $osmocombb_path/src/host/osmocon/osmocon $bin_path 
cp $osmocombb_path/src/host/layer23/src/misc/ccch_scan $bin_path 
cp $osmocombb_path/src/target/firmware/board/compal_e88/layer1.compalram.bin $bin_path
cp $osmocombb_path/src/host/layer23/src/misc/cell_log $bin_path
cp $osmocombb_path/src/host/gprsdecode/gprsdecode $bin_path

