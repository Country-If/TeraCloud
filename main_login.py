#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import hashlib
import os
import sys
from threading import Thread

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox

from TeraCloud import TeraCloud
from Signal import MySignals


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
        self.mySignals = MySignals()
        self.msgBox = QMessageBox(parent=self.ui)

        # 信号与槽连接
        self.mySignals.inform_signal.connect(self.inform)
        self.mySignals.login_success_signal.connect(self.success_login)
        self.mySignals.login_fail_signal.connect(self.fail_login)

    def login(self):
        """
        登录

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
            self.login_check(username, password)

    def login_check(self, username, password):
        """
        登录检查

        :param username: 用户名
        :param password: 密码
        :return: bool
        """

        def inform_thread():
            self.mySignals.inform_signal.emit()

        def login_check_thread():
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
                    self.mySignals.login_success_signal.emit()
                else:
                    self.mySignals.login_fail_signal.emit()
            else:
                self.mySignals.login_fail_signal.emit()

        # 判断文件是否存在
        if not os.path.exists('Account/main.txt'):
            self.ui.Login_btn.setEnabled(False)
            thread1 = Thread(target=inform_thread)
            thread2 = Thread(target=login_check_thread)
            thread1.start()
            thread2.start()
        else:
            with open('Account/main.txt', 'r') as f:
                username_fromFile = f.readline().strip()
                password_hash = f.readline().strip()
                capacity_fromFile = f.readline().strip()
            if username_fromFile == username and password_hash == hashlib.md5(password.encode('utf-8')).hexdigest():
                self.username = username
                self.capacity = capacity_fromFile
                self.login_status = True
                self.ui.close()
            else:
                self.login_status = False
                QMessageBox.critical(self.ui, '错误', '登录失败')

    def inform(self):
        """
        验证信息系提醒

        :return: None
        """
        self.msgBox.setWindowTitle('提示')
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.setText('正在验证账号信息，请耐心等待...')
        self.msgBox.exec()

    def success_login(self):
        """
        登录成功

        :return: None
        """
        self.ui.Login_btn.setEnabled(True)
        self.msgBox.button(QMessageBox.Ok).animateClick()
        self.login_status = True
        self.ui.close()

    def fail_login(self):
        """
        登录失败

        :return: None
        """
        self.ui.Login_btn.setEnabled(True)
        self.msgBox.button(QMessageBox.Ok).animateClick()
        self.login_status = False
        QMessageBox.critical(self.ui, '错误', '登录失败')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_login_ui()
    window.ui.show()
    app.exec_()
