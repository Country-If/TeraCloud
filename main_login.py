#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import sys
import hashlib
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox


class Main_login_ui:
    """main login UI"""

    def __init__(self):
        """
        实例化对象
        """
        # 动态加载界面
        self.ui = uic.loadUi("UI/main_login.ui")
        self.ui.Login_btn.clicked.connect(self.login)

        # 其他属性
        self.login_status = False
        self.username = None
        self.password = None

    def login(self):
        self.input_check()

    def input_check(self):
        """
        检查输入

        :return: None
        """
        # 获取输入框文本
        username = self.ui.userid.text().strip()
        password = self.ui.passwd.text().strip()

        # 对输入信息进行检查
        if username == '':
            QMessageBox.critical(self.ui, '错误', '用户名不能为空')
        elif password == '':
            QMessageBox.critical(self.ui, '错误', '密码不能为空')
        elif ',' in username or ',' in password:
            QMessageBox.critical(self.ui, '错误', '含有非法字符')
        else:
            self.login_status = True
            self.username = username
            self.password = hashlib.md5(password.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_login_ui()
    window.ui.show()
    app.exec_()
