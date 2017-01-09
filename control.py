# coding=utf-8

import subprocess
import time
import getopt
from sys import argv, path

class control_c118(object) :
    def __init__(self) :
        '''
        @get the current path
        @get the current usb port
        @set the new terminal command
        '''
        self.current_path = path[0]
        self.usbs = self.getusb()
        self.terminal = ['gnome-terminal', '-t', 'noname', '-e']

    def setTerminalName(self, name) :
        '''
        set the new terminal name.
        '''
        self.terminal[2] = name

    def getTerminalCommand(self, cmd) :
        self.terminal.append(cmd)
        return self.terminal

    def runCommand(self, cmd) :
        '''
        start a new terminal.
        '''
        sub = None
        try :
            sub = subprocess.Popen(cmd, stderr = subprocess.PIPE, stdout = subprocess.PIPE)
        except Exception, e:
            print "error : %s" % str(e)

        return sub

    def runCommand2(self, cmd) :
        '''
        run shell command.
        '''
        sub = None
        try :
            sub = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE)
        except Exception, e:
            print "error : %s" % str(e)

        return sub

    def getusb(self):
        '''
        get the usb list.
        '''
        usblist = []
        
        cmd = 'ls /dev | grep ttyUSB'
        subpro2 = self.runCommand2(cmd) 
        subpro2.wait()
        ttylog = subpro2.communicate()

        ttyusbList = ttylog[0].split('\n')

        del ttyusbList[len(ttyusbList)-1]

        for u in range(len(ttyusbList)):
                    usblist.append('/dev/'+ttyusbList[u])

        return usblist

    def download(self, usb_list = None) :
        '''
        download the rom to the mobile.
        '''
        if usb_list is None :
            usb_list = self.usbs
        for usb in usb_list :
            dev = usb[-4:]
            down_cmd = "sudo %s/c118/osmocon -m c123xor -p %s -s /tmp/osmocom_l2_%s %s/c118/layer1.compalram.bin"  % (self.current_path, usb, dev, self.current_path)
            self.setTerminalName('osmocon for ' + dev)
            cmd = self.getTerminalCommand(down_cmd)
            downloadprocess = self.runCommand(cmd) 
            time.sleep(1)
        return 0 

    def sniffer(self, usb_list, port_list) :
        '''
        start sniffer the port.
        '''
        if usb_list is None :
            usb_list = self.usbs
        lu = len(usb_list)
        lp = len(port_list)
        l = lp
        if lu < lp :
            l = lu
        for i in range(0, l) :
            dev = usb_list[i][-4:]
            sniffer_cmd = "sudo %s/c118/ccch_scan -a %s -s /tmp/osmocom_l2_%s" % (self.current_path, port_list[i], dev)
            self.setTerminalName('sniffer for %s' % port_list[i])
            cmd = self.getTerminalCommand(sniffer_cmd)
            snifferprocess = self.runCommand(cmd) 

        return 0

    def gprsdecode(self, file_list):
        '''
        start decode the gprs data.
        the data read from the file list.
        '''
        for file_name in file_list :
            file_cmd = "sudo %s/c118/gprsdecode %s" % (self.current_path, file_name)
            self.setTerminalName('decode gprs from data file')
            cmd = self.getTerminalCommand(file_cmd)
            fileprocess = self.runCommand(cmd)
            
        return 0

    def gprsdecodePipe(self) :
        '''
        start decode the gprs data.
        the data read from the pipe and it's real time. 
        '''
        file_cmd = "sudo %s/c118/gprsdecode" % self.current_path
        self.setTerminalName('decode gprs from pipe')
        cmd = self.getTerminalCommand(file_cmd)
        fileprocess = self.runCommand(cmd) 

        return 0

    def startWireshark(self):
        '''
        start a new wireshark to capture the mac/rlc data.
        '''
        wire_cmd = "sudo wireshark -k -i lo -f \'port 4729\'"
        self.setTerminalName('start wiershark')
        cmd = self.getTerminalCommand(wire_cmd)
        wiresharkprocess = self.runCommand(cmd)

        return 0

    def killAll(self) :
        '''
        kill all processes.
        '''
        cmd = 'sudo killall ccch_scan cell_log gprsdecode 2>/dev/null'
        lay23_proc = self.runCommand2(cmd)
        lay23_proc.wait()
        cmd = 'sudo killall osmocon 2>/dev/null'
        osmc_proc = self.runCommand2(cmd) 

    def removeData(self):
        '''
        remove the all data file.
        '''
        cmd = 'sudo rm *.dat'
        rmproc = self.runCommand2(cmd)

def usage():
    print '''
    control.py usage:
    -h,--help : print help message
    -v,--version : print current version
    -f,--function : which function could be used (down/sniff/gprs/wireshark/kill/rm)
        down : download the rom to mobile
        sniff : sniffer the ARFCN followd the sniff
        gprs : decode the signal.if nothing followd the gprs ,it could be use on real time.or the data file should be followd by gprs.
        wireshark : start the wireshark to capture the GSM data.
        kill : stop the all process.
        rm : remove the all data file.
        use like :  sudo python control.py -f down
                    sudo python control.py -f sniff [47 47 56 ...]
                    sudo python control.py -f gprs [data1.dat  data2.dat ...]
                    sudo python control.py -f wireshark
                    sudo python control.py -f kill
                    sudo python control.py -f rm
    '''

def version():
    print '''
    control.py version 1.0.1
    '''

def function(v, args):
    print '''
    call the function.
    function : %s
    ''' % (v)
    c118 = control_c118()
    if v == 'down' :
        c118.download()
    elif v == 'sniff' :
        c118.sniffer(None, args)
    elif v == 'gprs' :
        if args == [] :
            c118.gprsdecodePipe()
        else :
            c118.gprsdecode(args)
    elif v == 'wireshark' :
        c118.startWireshark()
    elif v == 'kill' :
        c118.killAll()
    elif v == 'rm' :
        c118.removeData()
        

def main():
    try :
        opts, args = getopt.getopt(argv[1:], 'hvf:', ['help', 'version', 'function='])
    except Exception, e:
        usage()
        exit(0)
    for name, value in opts :
        if name in ('-h', '--help') :
            usage()
        if name in ('-v', '--version') :
            version()
        if name in ('-f', '--function') :
            function(value, args)

if __name__ == "__main__" :
    main()
