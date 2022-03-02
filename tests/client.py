# -*- coding=utf-8 -*-

"""
file: send.py
socket client
"""

import socket
import os
import struct
import pickle
import random
import string
from time import ctime, time
from gmssl import sm9
import json


def socket_client():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # IP = input('请输入对方主机IP地址：')
        # Port = int(input('请输入端口号：'))
        IP = '127.0.0.1'
        Port = int(6666)
        s.connect((IP, Port))
    except socket.error as msg:
        print(msg)
        sys.exit()

    print(s.recv(1024).decode("utf-8"))
    # pubdata = s.recv(1024)
    # pubkey = pickle.loads(pubdata)
    # secret_key = ''.join(random.sample(string.ascii_letters + string.digits, 8))  # 随机生成长度为8的des密钥
    # crypto = rsa.encrypt(secret_key.encode(), pubkey)
    # s.send(crypto)

    # master_public, master_secret = sm9.setup('encrypt')
    # Da = sm9.private_key_extract('encrypt', master_public, master_secret, idA)
    # message = 'abc'
    # ct = sm9.kem_dem_enc(master_public, idA, message, 32)
    # s.send(master_public)
    # s.send(idA)
    # s.send(Da)
    # s.send(ct)

    # pt = sm9.kem_dem_dec(master_public, idA, Da, ct, 32)

    while True:
        p_master_public = s.recv(2048)
        print(p_master_public)
        print(len(p_master_public))

        pp_dict = s.recv(1024)
        print(pp_dict)
        print(len(pp_dict))
        p_dict = pickle.loads(pp_dict)
        p_idA = p_dict['idA']
        p_Da = p_dict['Da']
        p_ct = p_dict['ct']
        # p_idADact = s.recv(1024)
        # p_idA = p_idADact[0, 15]
        # p_Da = p_idADact[16, 203]
        # p_ct = p_idADact[]
        # p_idA = s.recv(1024)
        # print(p_idA)
        # print(len(p_idA))
        # p_Da = s.recv(1024)
        # print(p_Da)
        # print(len(p_Da))
        # p_ct = s.recv(1024)
        # print(len(p_ct))
        # print(p_ct)
        master_public = pickle.loads(p_master_public)
        idA = pickle.loads(p_idA)
        Da = pickle.loads(p_Da)
        ct = pickle.loads(p_ct)

        pt = sm9.kem_dem_dec(master_public, idA, Da, ct, 32)

        s.send('完成数据接受并解密成功'.encode())
        print('接收到的数据为'+pt)
        print(s.recv(1024).decode("utf-8"))
        s.send('结束本次通信'.encode())
        s.close()
        break


def transInfo(data, pubkey, cli):
    ##======加密部分======###
    master_public, master_secret = sm9.setup('encrypt')
    Da = sm9.private_key_extract('encrypt', master_public, master_secret, idA)
    message = 'abc'
    ct = sm9.kem_dem_enc(master_public, idA, message, 32)
    pt = sm9.kem_dem_dec(master_public, idA, Da, ct, 32)

    assert (message == pt)

    cli.send(data1)  # 传输加密后的数据
    cli.send(crypto)  # 传输加密的des密钥


def generateSM9EncryptKeys(idA):
    master_public, master_secret = sm9.setup('encrypt')
    Da = sm9.private_key_extract('encrypt', master_public, master_secret, idA)

    start = time()
    return pubkey, privkey, start


if __name__ == '__main__':
    socket_client()
