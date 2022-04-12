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
        p_dict = pickle.loads(pp_dict) #得到字典数据
        p_idA = p_dict['idA']
        p_Da = p_dict['Da']
        p_ct = p_dict['ct']
        master_public = pickle.loads(p_master_public)
        idA = pickle.loads(p_idA)
        Da = pickle.loads(p_Da)
        ct = pickle.loads(p_ct)

        pt = sm9.kem_dem_dec(master_public, idA, Da, ct, 32)

        s.send('完成数据接受并解密成功'.encode())
        print('接收到的数据为'+pt)


        ##签名验签
        s_master_public, s_master_secret = sm9.setup ('sign')
        s_Da = sm9.private_key_extract ('sign', s_master_public, s_master_secret, idA)
        signature = sm9.sign (s_master_public, s_Da, pt)

        p_s_master_public = pickle.dumps(s_master_public)
        p_s_message = pickle.dumps(pt)
        p_s_idA = pickle.dumps(idA)
        p_signature = pickle.dumps(signature)
        p_s_dict = {'idA': p_s_idA, 'message': p_s_message, 'signature': p_signature}
        pp_s_dict = pickle.dumps(p_s_dict)
        s.send(p_s_master_public)
        s.send(pp_s_dict)

        # assert (sm9.verify (master_public, idA, message, signature))
        # 1/0 ← Verify(mpk, M, σ, ID).验证算法Verify以系统主公钥mpk、签名消息M及其签名σ和签名者的标识ID
        # 为输入, 输出“1”或者“0”.“1”表示签名有效,“0”表示签名无效.此算法由验证者执行.
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
