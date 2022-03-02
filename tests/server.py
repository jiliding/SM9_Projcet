# -*- coding=utf-8 -*-

"""
file: recv.py
socket service
"""
import socket
import threading
import time
import sys
import os
import struct
import pickle
from gmssl import sm9
import json
idA = 'a'
def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('127.0.0.1', 6666))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print('正在等待连接......')

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=deal_data, args=(conn, addr))
        t.start()


def deal_data(conn, addr):
    print('已连接到主机： {0}'.format(addr))
    # conn.settimeout(500)
    conn.send('Hi, Welcome to the server!'.encode("utf-8"))



    # (pubkey, privkey) = rsa.newkeys(1024)  # RSA生成密钥
    # pubdata = pickle.dumps(pubkey)
    # conn.send(pubdata)
    # descry = conn.recv(1024)
    # deskey = rsa.decrypt(descry, privkey).decode()


    while True:
        master_public, master_secret = sm9.setup('encrypt')
        Da = sm9.private_key_extract('encrypt', master_public, master_secret, idA)
        message = 'abc'
        ct = sm9.kem_dem_enc(master_public, idA, message, 32)
        p_master_public = pickle.dumps(master_public)
        p_idA = pickle.dumps(idA)
        p_Da = pickle.dumps(Da)
        p_ct = pickle.dumps(ct)
        start_time = time.time()
        p_dict = {'idA': p_idA, 'Da': p_Da, 'ct': p_ct}
        pp_dict = pickle.dumps(p_dict)
        print(pp_dict)
        print(len(pp_dict))
        # print(len(p_master_public))
        # print(len(p_idA))
        # print(len(p_Da))
        # print(len(p_ct))
        # print(p_master_public)
        # print(p_idA)
        # print(p_Da)
        # print(p_ct)
        conn.send(p_master_public)
        conn.send(pp_dict)
        # conn.send(p_idA)
        # conn.send(p_Da)
        # conn.send(p_ct)
        print(conn.recv(1024).decode('utf-8'))
        end_time = time.time()
        if (end_time - start_time > 5):
            print('连接出错，中断连接，终端类型：与客户端连接超时')
            conn.close()
            break


        conn.send('已发送'.encode("utf-8"))
        print('已发送')
        # print('已发送'.encode("utf-8"))
        print('通信时间：', time.ctime())
        print(conn.recv(1024).decode('utf-8'))
        conn.close()
        break


if __name__ == '__main__':
    socket_service()