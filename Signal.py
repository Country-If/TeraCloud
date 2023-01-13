#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

from PyQt5.QtCore import pyqtSignal, QObject


class MySignals(QObject):
    """自定义信号类"""
    inform_signal = pyqtSignal()
    login_success_signal = pyqtSignal()
    login_fail_signal = pyqtSignal()

    login2main_signal = pyqtSignal()

    subAccount_login_success = pyqtSignal(str, str)

    sync_success_signal = pyqtSignal(str)
    sync_fail_signal = pyqtSignal(str)
    time_out_signal = pyqtSignal()
    sync_time_out_signal = pyqtSignal(str)
