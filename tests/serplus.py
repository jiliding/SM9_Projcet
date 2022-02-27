# _*_coding:utf-8_*_
from socket import *
from time import ctime, time
from pyDes import *
import rsa
#import chardet
import pickle

def linkClient():
    host = '127.0.0.1'
    port = 1919
    buffer = 1024
    addr = (host, port)
    ser = socket(AF_INET, SOCK_STREAM)  # 创建流式套接字
    ser.bind(addr)  # 套接字绑定地址
    ser.listen(5)
    return ser, buffer
def generateRsaKeys():
    (pubkey, privkey) = rsa.newkeys(512)

    start = time()
    return pubkey, privkey, start

def sendKey(cli, pubkey):

    pubdata = pickle.dumps(pubkey)

    cli.send(pubdata)  # 将公钥封装发送
    return

def transInfo(cli, buffer, privkey):
    data = cli.recv(buffer)  # 接收加密后的数据
    descry = cli.recv(buffer)  # 接受加密后的des密钥
    deskey = rsa.decrypt(descry, privkey).decode()
    iv = deskey  # 向量
    k = des(deskey, CBC, iv, pad=None, padmode=PAD_PKCS5)  # 得到DES 对象
    data1 = k.decrypt(data)
    print('密文 >', data)
    print('明文 >', data1.decode())
    return data1

def createSignature(cli, data1, privkey):
    signature = rsa.sign(data1, privkey, 'SHA-1')  # 生成电子签名
    if data1.decode() == 'exit':
        print('退出成功')
        cli.close()
    cli.send(signature)
    cli.send((ctime()).encode())
    cli.send(data1)
    return

while True:
    print('waiting for connection....')
    ser, buffer = linkClient()

    cli, addr = ser.accept()
    print('.....connected from : ', addr)
    pubkey, privkey, start = generateRsaKeys()

    while True:
        end = time()
        if (end - start > 10):
            pubkey, privkey, start = generateRsaKeys()
            print(pubkey)  ##当两次通信时间大于10s时，自动更换密钥。
        sendKey(cli, pubkey)
        data1 = transInfo(cli, buffer, privkey)
        createSignature(cli, data1, privkey)

    cli.close()

ser.close()
# cli.send('%s %s' % (ctime(), data))
##已完成动态刷新，cs架构单方向通信。