#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import os
import datetime


def sync_time():
    """
    write the current time into file

    :return: None
    """
    if not os.path.exists("Data"):
        os.mkdir("Data")
    with open("Data/last_sync_time.txt", 'w') as f:
        f.write(datetime.datetime.now().strftime('%Y-%m-%d') + '\n')
        f.close()


def load_sync_time():
    """
    load sync time from file

    :return: sync time
    """
    if not os.path.exists('Data/last_sync_time.txt'):
        return None
    with open('Data/last_sync_time.txt', 'r') as f:
        load_time = f.readline().strip()
        f.close()
    return load_time
