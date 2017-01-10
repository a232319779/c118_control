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

    def runCommand(self, cmd, shell = False) :
        '''
        if shell is False, start a new terminal.
        else run as shell.
        '''
        sub = None
        try :
            sub = subprocess.Popen(cmd, shell = shell, stderr = subprocess.PIPE, stdout = subprocess.PIPE)
        except Exception, e:
            print "error : %s" % str(e)

        return sub

    def getusb(self):
        '''
        get the usb list.
        '''
        usblist = []
        
        cmd = 'ls /dev | grep ttyUSB'
        subpro2 = self.runCommand(cmd, True) 
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

    def sniffer(self, args) :
        '''
        start sniffer the port.
        '''
        usb_list = self.usbs
        lu = len(usb_list)
        lp = len(args)
        l = lp
        if lu < lp :
            l = lu
        for i in range(0, l) :
            dev = usb_list[i][-4:]
            sniffer_cmd = "sudo %s/c118/ccch_scan -a %s -s /tmp/osmocom_l2_%s" % (self.current_path, args[i], dev)
            print sniffer_cmd
            self.setTerminalName('sniffer for %s' % args[i])
            cmd = self.getTerminalCommand(sniffer_cmd)
            snifferprocess = self.runCommand(cmd) 

        return 0

    def gprsdecode(self, args):
        '''
        start decode the gprs data.
        '''
        file_cmd = "sudo %s/c118/gprsdecode %s" % (self.current_path, args)
        print file_cmd
        self.setTerminalName('decode gprs')
        cmd = self.getTerminalCommand(file_cmd)
        fileprocess = self.runCommand(cmd)
            
        return 0

    def startWireshark(self):
        '''
        start a new wireshark to capture the mac/rlc data.
        '''
        wire_cmd = "sudo wireshark -k -i lo -c \'port 4729\'"
        self.setTerminalName('start wiershark')
        cmd = self.getTerminalCommand(wire_cmd)
        wiresharkprocess = self.runCommand(cmd)

        return 0

    def killAll(self) :
        '''
        kill all processes.
        '''
        cmd = 'sudo killall ccch_scan cell_log gprsdecode 2>/dev/null'
        lay23_proc = self.runCommand(cmd, True)
        lay23_proc.wait()
        cmd = 'sudo killall osmocon 2>/dev/null'
        osmc_proc = self.runCommand(cmd, True) 

    def removeData(self):
        '''
        remove the all data file.
        '''
        cmd = 'sudo rm *.dat'
        rmproc = self.runCommand(cmd, True)

def usage():
    print '''
    control.py usage:
    -h,--help : print help message
    -v,--version : print current version
    -c,--cunction : which function could be used (down/sniff/gprs/wireshark/kill/rm)
        down : download the rom to mobile
        sniff : sniffer the ARFCN followd the sniff
        gprs : decode the signal.if nothing followd the gprs ,it could be use on real time.or the data file should be followd by gprs.
        wireshark : start the wireshark to capture the GSM data.
        kill : stop the all process.
        rm : remove the all data file.
        use like :  sudo python control.py -c down
                    sudo python control.py -c sniff [arfcn arfcn ...]
                    sudo python control.py -c gprs [opt ...]
                    sudo python control.py -c wireshark
                    sudo python control.py -c kill
                    sudo python control.py -c rm
    '''

def version():
    print '''
    control.py version 1.0.1
    '''
def parse2param(args) :
    args[0] = args[0][1:]
    args[-1] = args[-1][0:-1]
    return args

def function(v, args):
    print '''
    call the function.
    function : %s
    ''' % (v)
    
    c118 = control_c118()
    if v == 'down' :
        c118.download()
    elif v == 'sniff' :
        c118.sniffer(args)
    elif v == 'gprs' :
        c118.gprsdecode("".join(args))
    elif v == 'wireshark' :
        c118.startWireshark()
    elif v == 'kill' :
        c118.killAll()
    elif v == 'rm' :
        c118.removeData()
        

def main():
    try :
        opts, args = getopt.getopt(argv[1:], 'hvc:', ['help', 'version', 'call='])
    except Exception, e:
        usage()
        exit(0)
    for name, value in opts :
        if name in ('-h', '--help') :
            usage()
            break
        if name in ('-v', '--version') :
            version()
            break
        if name in ('-c', '--call') :
            args = parse2param(args)
            print args
            function(value, args)
            break

if __name__ == "__main__" :
    main()
