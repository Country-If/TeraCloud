#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

from PyQt5.QtCore import pyqtSignal, QObject


class MainLoginSignals(QObject):
    """Main Login Signals Class"""
    inform_signal = pyqtSignal()
    login_success_signal = pyqtSignal()
    login_fail_signal = pyqtSignal()
    time_out_signal = pyqtSignal()
    login2main_signal = pyqtSignal()


class SubAccountLoginSignals(QObject):
    """SubAccount Login Signals Class"""
    inform_signal = pyqtSignal()
    login_success_signal = pyqtSignal()
    login_fail_signal = pyqtSignal()
    time_out_signal = pyqtSignal()
    subAccount_login_success = pyqtSignal(str, str)


class MainUI_Signals(QObject):
    """Main UI Signals Class"""
    inform_signal = pyqtSignal()
    login_success_signal = pyqtSignal()

    sync_success_signal = pyqtSignal(int, str)
    sync_fail_signal = pyqtSignal(int, str)
    sync_time_out_signal = pyqtSignal(int, str)
    sync_stop_signal = pyqtSignal()
