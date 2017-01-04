# coding=utf-8


def read_txt(filename) :
    f = open(filename,'rb')
    txt = f.readlines()
    f.close()

    tmp = set(txt)
    rlcmac_data = [x.split('\t') for x in tmp]    
    rlcmac_data = [[int(x[0]),int(x[1]),x[2]] for x in rlcmac_data]

    return rlcmac_data

def p(rlcmac_data) :
    tmp = sorted(rlcmac_data)
    a = -1
    i = -1
    text2pacp = []
    for x in tmp :
        #print x
        if(a != x[0]) or '43c0' == x[2][0:4]:
            text2pacp.append('')
            i += 1
            a = x[0]
        xx = x[2].strip('\n').split(',')
        j = 0
        for xxx in xx :
            if 1 == j : 
                text2pacp.append('')
                i += 1
            text2pacp[i] += xxx
            j += 1

    for ddd in text2pacp :
        ppp = ddd.find('2b2b')
        if ppp != -1 :
            ddd = ddd[0:ppp]
        l = len(ddd)
        out = '0000 '
        for jj in range(0, l, 2) :
            out += (ddd[jj:jj+2] + ' ')
        print out


if __name__ == '__main__' :
    from sys import argv 
    rlcmac_data = read_txt(argv[1])
    p(rlcmac_data)
