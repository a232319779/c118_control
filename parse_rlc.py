# coding=utf-8

'''
    parse the RLC/MAC layer data.
    try to find the whole LLC layer data.

    define RLC/MAC data format : rlc_mac_data = {'TFI':chr, 'BSN':chr, 'FBI':chr, 'ME':chr, 'data':string}
    define RLC/MAC data set : rlc_mac_set = {ord:rlc_mac_data}
    define LLC data format : llc_data = {'TFI':chr, 'BSN':list, 'FBI':int, 'MISSING_BSN':list,'data':list}
    define LLC set format : llc_set = {ord:llc_data}
'''
class rlc_mac_parse(object) :
    def __init__(self) :
        '''
            must be the squence ,when use tshark to filter the pcap file,should use the command :
            tshark -r $pcap_file_name -R '(gsm_rlcmac.dl_payload_type==0)' -T fields -w out.pcap -e gsm_rlcmac.dl.tfi -e gsm_rlcmac.bsn -e gsm_rlcmac.fbi -e gsm_rlcmac.me -e data "
        '''
        self.key_words = ['TFI', 'BSN', 'FBI', 'ME', 'data']
        #self.current_llc_data = {'TFI':'0', 'BSN':[], 'FBI':'0', 'MISSING_BSN':[], 'ME':'', 'data':[]}
        self.rlc_mac_datas = {}
        self.rlc_mac_set = {}
        self.llc_set = {}
        self.current_ord = 0
        self.rlc_mac_count = 0
        self.llc_count = 0

    def read_txt_file(self, txt_file_name):
        '''
            read txt_file to get the rlc_mac_datas
            txt_file should be match the following conditions:
            use tshark ,and stdout by terminal pipe,like : tshark xxxxx > out.txt
        '''
        f = open(txt_file_name, 'rb')
        txt_lines = f.readlines()
        f.close()
       
        i = 0
        for each_line in txt_lines:
            each_line = each_line.strip('\n').split("\t")
            self.rlc_mac_datas[i] = dict(zip(self.key_words, each_line))
            i += 1
        # save the rlc_mac count
        self.rlc_mac_count = i

    def get_value(self, i, key = 'TFI') :
        '''
            key should be : 'TFI', 'BSN', 'FBI', 'ME', 'data'
            default : 'TFI'
        '''
        return self.rlc_mac_set[i][key]

    def get_TFI(self, i) :
        return self.get_value(i, 'TFI')

    def get_BSN(self, i) :
        return self.get_value(i, 'BSN')

    def get_FBI(self, i) :
        return self.get_value(i, 'FBI')

    def get_ME(self, i) :
        return self.get_value(i, 'ME')

    def get_data(self, i) :
        return self.get_value(i, 'data')

    # is the union packet data
    def is_union_data(self, i) :
        if len(self.rlc_mac_set) == 0:
            return 1
        for key, value in self.rlc_mac_set.items():
            if 0 == cmp(value, self.rlc_mac_datas[i]):
                return 0
        return 1

    # get union packet data set
    def get_union_rlc_mac_set(self):
        '''
        when the funciont finished.The self.rlc_mac_count change to the len(self.rlc_mac_set)
        save the union packet in self.rlc_mac_set
        :return: None
        '''
        rlc_count = 0
        while self.current_ord < self.rlc_mac_count:
            is_new = self.is_union_data(self.current_ord)
            if 1 == is_new:
                self.rlc_mac_set[rlc_count] = self.rlc_mac_datas[self.current_ord]
                rlc_count += 1
            self.current_ord += 1
        self.rlc_mac_count = rlc_count

    def get_BSN_squence(self):
        i = 0
        while i < self.rlc_mac_count:
            self.llc_set[self.llc_count] = {}
            self.llc_set[self.llc_count]['TFI'] = self.get_TFI(i)
            self.llc_set[self.llc_count]['BSN'] = []
            self.llc_set[self.llc_count]['FBI'] = 0
            self.llc_set[self.llc_count]['BSN_DATA'] = {}
            self.llc_set[self.llc_count]['BSN_ME'] = {}
            self.llc_set[self.llc_count]['data'] = []
            if self.get_FBI(i) == '1':
                self.llc_set[self.llc_count]['FBI'] = 1
            j = i
            while 1:
                if j >= self.rlc_mac_count:
                    return
                if self.llc_set[self.llc_count]['TFI'] != self.get_TFI(j):
                    break
                self.llc_set[self.llc_count]['BSN'].append(self.get_BSN(j))
                self.llc_set[self.llc_count]['BSN_DATA'][self.get_BSN(j)] = self.get_data(j)
                self.llc_set[self.llc_count]['BSN_ME'][self.get_BSN(j)] = self.get_ME(j)
                if self.get_FBI(j) == '1':
                    self.llc_set[self.llc_count]['FBI'] = 1
                j += 1
            i = j
            self.llc_count += 1

    def sort_BSN(self):
        for key,value in self.llc_set.items():
            self.llc_set[key]['BSN'] = sorted(value['BSN'])

    def join_data(self):
        for key,value in self.llc_set.items() :
            self.llc_set[key]['data'] = ['']
            i = 0
            for bsn in value['BSN'] :
                if value['BSN_ME'][bsn] == '3' :
                    i += 1
                    self.llc_set[key]['data'].append('')
                    data_list = value['BSN_DATA'][bsn].split(",")
                    self.llc_set[key]['data'][0] += data_list[0]
                    self.llc_set[key]['data'][1] += data_list[1]
                elif value['BSN_ME'][bsn] == '1' :
                    data_replace = value['BSN_DATA'][bsn].replace(",","")
                    self.llc_set[key]['data'][i] += data_replace
                else :
                    self.llc_set[key]['data'][i] += value['BSN_DATA'][bsn]

    def cpy_new_llc(self,i, j):
        self.llc_set[j]['TFI'] = self.rlc_mac_set[i]['TFI']
        self.llc_set[j]['FBI'] = self.rlc_mac_set[i]['FBI']
        self.llc_set[j]['BSN'] = [self.rlc_mac_set[i]['TFI']]
        if self.rlc_mac_set[i]['ME'] == 3:
            self.llc_set[j]['data'] = self.rlc_mac_set[i]['data'].splie(",")
        else:
            self.llc_set[j]['data'] = [self.rlc_mac_set[i]['data'].replce(",", "")]

    def run(self):
        # get union packet data
        self.get_union_rlc_mac_set()

        # get BSN sequence
        self.get_BSN_squence()

        # sort
        self.sort_BSN()

        # join data
        self.join_data()

    def write_txt_2_pacp(self):
        f = open('text_2_pacp.txt','wb')
        for value in self.llc_set.values() :
            for data in value['data'] :
                out = "0000 "
                l = len(data)
                for i in range(0, l - 2, 2) :
                    out += (data[i:i+2] + " ")
                out += '\n'
            f.write(out)
        f.close()
    
    def print_rlc(self):
        for key,value in self.rlc_mac_datas.items():
            print key,value

    def print_llc(self) :
        for key,value in self.llc_set.items() :
            print key, value

    def print_union_rlc(self):
        for key,value in self.rlc_mac_set.items():
            print key, value

    def print_llc_bsn_data(self):
        for key, value in self.llc_set.items() :
            print key, value['FBI'], value['BSN'], value['data']

if __name__ == "__main__":
    from sys import argv
    file_name = 'out.txt'
    if len(argv) > 1 :
        file_name = argv[1]
    rmp = rlc_mac_parse()
    rmp.read_txt_file(file_name)
    rmp.run()
    #rmp.print_rlc()
    #rmp.print_llc()
    #rmp.print_union_rlc()
    rmp.print_llc_bsn_data()
    rmp.write_txt_2_pacp()

