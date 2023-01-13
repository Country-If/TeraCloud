#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

from threading import Thread

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QMessageBox
from func_timeout.exceptions import FunctionTimedOut

from DES import encrypt
from Signal import MySignals
from TeraCloud import TeraCloud
from common import *


class SubAccount_login_ui(QDialog):
    """子账号登录"""

    def __init__(self, main_username):
        """
        实例化对象
        """
        # 动态加载界面
        super().__init__()
        uic.loadUi("UI/subAccount_login.ui", self)

        # 类属性
        self.msgBox = QMessageBox(parent=self)
        self.mySignals = MySignals()
        self.main_username = main_username
        self.add_username = None
        self.capacity = None

        # 信号与槽连接
        self.Login_btn.clicked.connect(self.login)
        self.mySignals.inform_signal.connect(self.inform)
        self.mySignals.login_success_signal.connect(self.success_login)
        self.mySignals.login_fail_signal.connect(self.fail_login)
        self.mySignals.time_out_signal.connect(self.time_out)

    def login(self):
        """
        subAccount login

        :return: None
        """
        # 获取输入框文本
        username = self.userid.text().strip()
        password = self.passwd.text().strip()

        # 对输入信息进行检查
        if username == '':
            QMessageBox.critical(self, '错误', '用户名不能为空')
        elif username == self.main_username:
            QMessageBox.critical(self, '错误', '主账号已登录')
        elif password == '':
            QMessageBox.critical(self, '错误', '密码不能为空')
        elif ',' in username or ',' in password:
            QMessageBox.critical(self, '错误', '含有非法字符')
        else:
            self.add_username = username
            self.login_check(username, password)

    def login_check(self, username, password):
        """
        subAccount login check

        :param username: username
        :param password: password
        :return: None
        """

        def inform_thread():
            """
            pop up information box thread
            """
            self.mySignals.inform_signal.emit()

        def login_check_thread():
            """
            login check thread
            """
            try:
                teraCloud = TeraCloud(username, password)
                flag, message = teraCloud.get_browser_source()
                if flag:
                    flag, capacity = teraCloud.get_capacity()
                    if flag:
                        write_sync_time()
                        # 写入文件
                        with open('Account/' + self.main_username + '/' + username + '.txt', 'w') as file:
                            file.write(username + '\n')
                            file.write(" ".join([str(i) for i in sum(encrypt(password, username), [])]) + '\n')
                            file.write(capacity + '\n')
                            file.close()
                        self.capacity = capacity
                        self.mySignals.login_success_signal.emit()
                    else:
                        self.mySignals.login_fail_signal.emit()
                else:
                    self.mySignals.login_fail_signal.emit()
            except FunctionTimedOut:
                self.mySignals.time_out_signal.emit()

        if os.path.exists('Account/' + self.main_username + '/' + username + '.txt'):
            QMessageBox.information(self, '提示', '该账号已存在')
        else:
            self.Login_btn.setEnabled(False)  # 禁用按钮
            thread1 = Thread(target=inform_thread)
            thread2 = Thread(target=login_check_thread)
            thread1.start()
            thread2.start()

    def inform(self):
        """
        验证信息系提醒

        :return: None
        """
        self.msgBox.setWindowTitle('提示')
        self.msgBox.setStandardButtons(QMessageBox.Ok)
        self.msgBox.setText('正在验证账号信息，请耐心等待，关闭该窗口将会在后台验证信息...')
        self.msgBox.exec()

    def success_login(self):
        """
        登录成功

        :return: None
        """
        self.Login_btn.setEnabled(True)  # 启用按钮
        self.msgBox.button(QMessageBox.Ok).animateClick()
        QMessageBox.information(self, '提示', self.add_username + ' 登录成功')
        self.mySignals.subAccount_login_success.emit(self.add_username, self.capacity)
        self.accept()

    def fail_login(self):
        """
        登录失败

        :return: None
        """
        self.Login_btn.setEnabled(True)  # 启用按钮
        self.msgBox.button(QMessageBox.Ok).animateClick()
        QMessageBox.critical(self, '错误', self.add_username + ' 登录失败')

    def time_out(self):
        """
        登录超时

        :return: None
        """
        self.Login_btn.setEnabled(True)
        self.msgBox.button(QMessageBox.Ok).animateClick()
        QMessageBox.critical(self, '错误', '连接超时')
