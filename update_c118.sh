folder="./c118"

if [ ! -x "$folder" ];then
    mkdir "$folder"
fi

cp ~/GSM/osmocom-bb/src/host/osmocon/osmocon "$folder" 
cp ~/GSM/osmocom-bb/src/host/layer23/src/misc/ccch_scan "$folder" 
cp ~/GSM/osmocom-bb/src/target/firmware/board/compal_e88/layer1.compalram.bin "$folder"
cp ~/GSM/osmocom-bb/src/host/layer23/src/misc/cell_log "$folder"
cp ~/GSM/osmocom-bb/src/host/gprsdecode/gprsdecode "$folder"

