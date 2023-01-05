#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import os
import sys
from threading import Thread
import hashlib
from TeraCloud import TeraCloud
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
        self.ui.passwd.returnPressed.connect(self.login)

        # 其他属性
        self.login_status = False
        self.username = None
        self.capacity = None

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
            if self.login_check(username, password):
                self.login_status = True
                self.ui.close()
            else:
                self.login_status = False
                QMessageBox.critical(self.ui, '错误', '登录失败')

    def login_check(self, username, password):
        """
        登录检查

        :param username: 用户名
        :param password: 密码
        :return: bool
        """
        # 判断文件是否存在
        if not os.path.exists('Account/main.txt'):
            # TODO: add threading
            teraCloud = TeraCloud(username, password)
            flag, message = teraCloud.get_browser_source()
            if flag:
                flag, capacity = teraCloud.get_capacity()
                if flag:
                    self.username = username
                    self.capacity = capacity
                    # 写入文件
                    if not os.path.exists("Account"):
                        os.mkdir("Account")
                    with open('Account/main.txt', 'w') as f:
                        f.write(username + '\n')
                        f.write(hashlib.md5(password.encode('utf-8')).hexdigest() + '\n')
                        f.write(capacity)
                    return True
                else:
                    return False
        else:
            with open('Account/main.txt', 'r') as f:
                username_ = f.readline().strip()
                password_ = f.readline().strip()
                capacity_ = f.readline().strip()
            if username_ == username and password_ == hashlib.md5(password.encode('utf-8')).hexdigest():
                self.username = username
                self.capacity = capacity_
                return True
            else:
                return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_login_ui()
    window.ui.show()
    app.exec_()
