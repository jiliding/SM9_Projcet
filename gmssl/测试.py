import binascii
from math import ceil, floor, log
def i2sp (m, l):
    format_m = ('%x' % m).zfill(l*2).encode('utf-8') #返回指定长度的字符串，原字符串右对齐，前面填充0，再转化为utf-8
    octets = [j for j in binascii.a2b_hex(format_m)] #十六进制转化为二进制
    octets = octets[0:l]
    return ''.join (['%02x' %oc for oc in octets]) #宽度为2的十六进制整数，左补零
def fe2sp (fe):
    fe_str = ''.join (['%x' %c for c in fe.coeffs])
    if (len(fe_str) % 2) == 1:
        fe_str = '0' + fe_str #长度变为偶数
    return fe_str

def ec2sp (P):
    ec_str = ''.join([fe2sp(fe) for fe in P])  ##将p转化为fe.coeffs?
    return ec_str

def str2hexbytes (str_in):
    return [b for b in str_in.encode ('utf-8')] #转化为utf-8编码

def h2rf (i, z, n):
    l = 8 * ceil ((5*bitlen(n)) / 32)
    msg = i2sp(i,1).encode('utf-8')
    ha = sm3_kdf (msg+z, l)
    h = int (ha, 16)
    return (h % (n-1)) + 1
if __name__ == '__main__':
    m = 'success'
    msg = i2sp(15, 1)
    print(msg,len(msg))