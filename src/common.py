#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import datetime
import os

from DES import decrypt, bit2string


def write_sync_time():
    """
    write the current time into file

    :return: None
    """
    if not os.path.exists("../Data"):
        os.mkdir("../Data")
    with open("../Data/last_sync_time.txt", 'w') as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%d') + '\n')
        f.close()


def load_sync_time():
    """
    load sync time from file

    :return: sync time
    """
    if not os.path.exists('../Data/last_sync_time.txt'):
        return None
    with open('../Data/last_sync_time.txt', 'r') as f:
        load_time = f.readline().strip()
        f.close()
    return load_time


def get_password_plaintext(username, passwd):
    """
    get password plaintext from encrypted str

    :param username: username
    :param passwd: encrypted password (str)
    :return: plaintext (str)
    """
    encrypt_list = []
    plaintext = ""
    tmp = passwd.split(' ')
    for i in range(0, len(tmp), 64):
        encrypt_list.append([int(bit) for bit in tmp[i:i + 64]])
    decrypt_list = decrypt(encrypt_list, username)
    for de in decrypt_list:
        plaintext += bit2string(de).strip('\x00')
    return plaintext
