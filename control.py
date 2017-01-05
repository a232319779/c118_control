import subprocess
import serial
import time
from sys import argv, path

class control_c118(object) :
    def __init__(self) :
        self.current_path = path[0]

    def getUSB(self):
        USBLIST = []

        subPro2 = subprocess.Popen('ls /dev | grep ttyUSB', shell=True,stdout = subprocess.PIPE)
        subPro2.wait()
        ttylog = subPro2.communicate()

        ttyusbList = ttylog[0].split('\n')

        del ttyusbList[len(ttyusbList)-1]

        for u in range(len(ttyusbList)):
                    USBLIST.append('/dev/'+ttyusbList[u])

        return USBLIST

    def download(self, usb_list) :
        for usb in usb_list :
            dev = usb[-4:]
            down_cmd = "sudo %s/c118/osmocon -m  \
            c123xor -p %s -s /tmp/osmocom_l2_%s \
            %s/c118/layer1.compalram.bin" % (self.current_path, usb, dev, self.current_path)
            try :
                downloadCommand = ['gnome-terminal', '-t', 'osmocom for ' + dev,'-e',\
                                  down_cmd]
                downloadProcess = subprocess.Popen(downloadCommand,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
                time.sleep(1)
            except Exception,e:
                print "error : %s " %  str(e)
                return -1
        return 0 

    def sniffer(self, usb_list,port_list) :
        lu = len(usb_list)
        lp = len(port_list)
        l = lp
        if lu < lp :
            l = lu
        for i in range(0, l) :
            dev = usb_list[i][-4:]
            sniffer_cmd = "sudo %s/c118/ccch_scan -a %s -s /tmp/osmocom_l2_%s" % (self.current_path, port_list[i], dev)
            sniffer_command = ['gnome-terminal', '-e', sniffer_cmd]
            try :
                snifferProcess = subprocess.Popen(sniffer_command,
                                              stderr=subprocess.PIPE,stdout=subprocess.PIPE)
            except Exception,e:
                print "error : %s" % str(e)
        return 0

    def gprsdecode(self, file_list):
        for file_name in file_list :
            file_cmd = "sudo %s/c118/gprsdecode %s" % (self.current_path, file_name)

            file_command = ['gnome-terminal', '-e', file_cmd]
            try :
                fileProcess = subprocess.Popen(file_command,
                                               stderr=subprocess.PIPE,stdout=subprocess.PIPE)
            except Exception,e :
                print "error : %s " % str(e)
        return 0

    def gprsdecode_pipe(self) :
        file_cmd = "sudo %s/c118/gprsdecode" % self.current_path
        file_command = ['gnome-terminal', '-e', file_cmd]
        try :
            fileProcess = subprocess.Popen(file_command, stderr = subprocess.PIPE, stdout = subprocess.PIPE)
        except Exception, e :
            print "error : %s" % str(e)
        return 0

    def start_wireshark(self):
        wire_cmd = "sudo wireshark -k -i lo -f \'port 4729\'"
        wire_command = ['gnome-terminal', '-t', 'wireshark', '-e' ,wire_cmd]
        subprocess.Popen(wire_command, stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE)

    def killall(self) :
        lay23_proc = subprocess.Popen("sudo killall ccch_scan cell_log 2>/dev/null", shell
                        = True)
        lay23_proc.wait()
        osmc_proc = subprocess.Popen("sudo killall osmocom 2>/dev/null", shell=True)

    def remove_data(self):
        subprocess.Popen("sudo rm *.dat", shell = True)


if __name__ == "__main__" :
    c118 = control_c118()
    usbs = c118.getUSB()
    if argv[1] == 'down' :
        print 'start download bb'
        c118.download(usbs)
    elif argv[1] == 'sniff' :
        print 'start sniff'
        port_list = ['47'] * 3
        if len(argv) > 3 :
            port_list = argv[2:]
        c118.sniffer(usbs, port_list)
    elif argv[1] == 'gprs' :
        print 'start gprs decode'
        if len(argv) < 3 :
            c118.gprsdecode_pipe()
            exit(0)
        c118.gprsdecode(argv[2:])
    elif argv[1] == 'wireshark':
        c118.start_wireshark()
    elif argv[1] == 'kill' :
        c118.killall()
    elif argv[1] == 'rm' :
        c118.remove_data()
