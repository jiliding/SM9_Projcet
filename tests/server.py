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
        conn.send(master_public)
        conn.send(idA)
        conn.send(Da)
        conn.send(ct)

        conn.send('已发送'.encode("utf-8"))
        print('通信时间：', time.ctime())
        print(conn.recv(1024).decode('utf-8'))
        conn.close()
        break


if __name__ == '__main__':
    socket_service()