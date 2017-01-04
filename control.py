import subprocess
import serial
import time

def getUSB():
    USBLIST = []

    subPro2 = subprocess.Popen('ls /dev | grep ttyUSB', shell=True,stdout = subprocess.PIPE)
    subPro2.wait()
    ttylog = subPro2.communicate()

    ttyusbList = ttylog[0].split('\n')

    del ttyusbList[len(ttyusbList)-1]

    for u in range(len(ttyusbList)):
		USBLIST.append('/dev/'+ttyusbList[u])

    return USBLIST

def download(usb_list) :
    for usb in usb_list :
        dev = usb[-4:]
        down_cmd = "sudo /home/newsun/GSM/control_python/c118/osmocon -m  \
        c123xor -p %s -s /tmp/osmocom_l2_%s \
        /home/newsun/GSM/control_python/c118/layer1.compalram.bin" % (usb, dev)
        try :
            downloadCommand = ['gnome-terminal', '-t', 'osmocom for ' + dev,'-e',\
                              down_cmd]
            downloadProcess = subprocess.Popen(downloadCommand,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
            time.sleep(1)
        except Exception,e:
            print "error : %s " %  str(e)
            return -1
    return 0 

def sniffer(usb_list,port_list) :
    lu = len(usb_list)
    lp = len(port_list)
    l = lp
    if lu < lp :
        l = lu
    for i in range(0, l) :
        dev = usb_list[i][-4:]
        sniffer_cmd = "sudo /home/newsun/GSM/control_python/c118/ccch_scan -a %s -s /tmp/osmocom_l2_%s" % (port_list[i], dev)
        sniffer_command = ['gnome-terminal', '-e', sniffer_cmd]
        try :
            snifferProcess = subprocess.Popen(sniffer_command,
                                          stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        except Exception,e:
            print "error : %s" % str(e)
    return 0

def gprsdecode(file_list):
    for file_name in file_list :
        file_cmd = "sudo /home/newsun/GSM/control_python/c118/gprsdecode %s" % file_name
        file_command = ['gnome-terminal', '-e', file_cmd]
        try :
            fileProcess = subprocess.Popen(file_command,
                                           stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        except Exception,e :
            print "error : %s " % str(e)
    return 0

def start_wireshark():
    wire_cmd = "sudo wireshark -k -i lo -f \'port 4729\'"
    wire_command = ['gnome-terminal', '-t', 'wireshark', '-e' ,wire_cmd]
    subprocess.Popen(wire_command, stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE)

def killall() :
    lay23_proc = subprocess.Popen("sudo killall ccch_scan cell_log 2>/dev/null", shell
                    = True)
    lay23_proc.wait()
    osmc_proc = subprocess.Popen("sudo killall osmocom 2>/dev/null", shell=True)

def remove_data():
    subprocess.Popen("sudo rm bursts_2016*", shell = True)


if __name__ == "__main__" :
    import sys
    usbs = getUSB()
    if sys.argv[1] == 'down' :
        print 'start download bb'
        download(usbs)
    elif sys.argv[1] == 'sniff' :
        print 'start sniff'
        port_list = ['47'] * 3
        if len(sys.argv) > 3 :
            port_list = sys.argv[2:]
        sniffer(usbs, port_list)
    elif sys.argv[1] == 'gprs' :
        print 'start gprs decode'
        if len(sys.argv) < 3 :
            print 'no data file'
            exit(0)
        gprsdecode(sys.argv[2:])
    elif sys.argv[1] == 'wireshark':
        start_wireshark()
    elif sys.argv[1] == 'kill' :
        killall()
    elif sys.argv[1] == 'rm' :
        remove_data()
