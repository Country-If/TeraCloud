#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox


class SubAccount_login_ui(QDialog):
    """子账号登录"""

    def __init__(self):
        """
        实例化对象
        """
        # 动态加载界面
        super().__init__()
        uic.loadUi("UI/subAccount_login.ui", self)

        # 信号与槽连接
        self.Login_btn.clicked.connect(self.login)

    def login(self):
        username = self.userid.text().strip()
        if username == 'admin':
            QMessageBox.information(self, '提示', '登录成功')
            self.accept()
