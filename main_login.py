#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import sys
from threading import Thread

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMessageBox
from func_timeout.exceptions import FunctionTimedOut

from DES import encrypt
from Signal import MainLoginSignals as MySignals
from TeraCloud import TeraCloud
from common import *


class Main_login_ui:
    """main login UI"""

    def __init__(self):
        """
        实例化对象
        """
        # 动态加载界面
        self.ui = uic.loadUi("UI/main_login.ui")
        self.ui.checkBox.setChecked(True)

        # 其他属性
        self.login_status = False
        self.username = None
        self.capacity = None
        self.last_sync_time = None
        self.mySignals = MySignals()
        self.msgBox = QMessageBox(parent=self.ui)
        self.remember_password = True

        # 信号与槽连接
        self.ui.Login_btn.clicked.connect(self.login)
        self.ui.passwd.returnPressed.connect(self.login)
        self.ui.checkBox.clicked.connect(self.checkBox_status_update)
        self.ui.auto_login_btn.clicked.connect(self.auto_login)
        self.mySignals.inform_signal.connect(self.inform)
        self.mySignals.login_success_signal.connect(self.success_login)
        self.mySignals.login_fail_signal.connect(self.fail_login)
        self.mySignals.time_out_signal.connect(self.time_out)

    def auto_login(self):
        """
        auto login: use last login information

        :return: None
        """
        if not os.path.exists("Account/main.txt"):
            QMessageBox.critical(self.ui, '错误', "未登录过，无法自动登录")
        else:
            # 读取信息
            with open('Account/main.txt', 'r') as f:
                self.username = f.readline().strip()
                f.readline()
                self.capacity = f.readline().strip()
                f.close()
            self.last_sync_time = load_sync_time()

            self.update_status(True)

    def checkBox_status_update(self):
        """
        update checkBox status when mouse clicked

        :return: None
        """
        check_state = self.ui.checkBox.checkState()
        if check_state == Qt.Checked:
            self.remember_password = True
        elif check_state == Qt.Unchecked:
            self.remember_password = False

    def update_status(self, status):
        """
        更新登录状态

        :param status: 登录状态
        :return: None
        """
        self.login_status = status

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
            """
            登录提示线程
            """
            self.mySignals.inform_signal.emit()

        def login_check_thread():
            """
            登录检查线程
            """
            try:
                teraCloud = TeraCloud(username, password)
                flag, message = teraCloud.get_browser_source()
                if flag:
                    flag, capacity = teraCloud.get_capacity()
                    if flag:
                        self.username = username
                        self.capacity = capacity
                        self.last_sync_time = datetime.datetime.now().strftime('%Y-%m-%d')
                        write_sync_time()
                        # 写入文件
                        if not os.path.exists("Account"):
                            os.mkdir("Account")
                        with open('Account/main.txt', 'w') as file:
                            file.write(username + '\n')
                            file.write(" ".join([str(i) for i in sum(encrypt(password, username), [])]) + '\n')
                            file.write(capacity + '\n')
                            file.close()
                        self.mySignals.login_success_signal.emit()
                    else:
                        self.mySignals.login_fail_signal.emit()
                else:
                    self.mySignals.login_fail_signal.emit()
            except FunctionTimedOut:
                self.mySignals.time_out_signal.emit()

        # 判断文件是否存在
        if not os.path.exists('Account/main.txt'):
            self.update_btn_status(False)  # 禁用按钮
            thread1 = Thread(target=inform_thread)
            thread2 = Thread(target=login_check_thread)
            thread1.start()
            thread2.start()
        else:
            # 读取信息
            with open('Account/main.txt', 'r') as f:
                username_fromFile = f.readline().strip()
                password_encrypted = f.readline().strip()
                capacity_fromFile = f.readline().strip()
                f.close()
            with open('Data/last_sync_time.txt', 'r') as f:
                last_sync_time = f.readline().strip()
                f.close()
            # 验证账号和密码的哈希值
            if username_fromFile == username \
                    and password_encrypted == " ".join([str(i) for i in sum(encrypt(password, username), [])]):
                self.username = username
                self.capacity = capacity_fromFile
                self.last_sync_time = last_sync_time
                self.update_status(True)
                self.mySignals.login2main_signal.emit()
                if not os.path.exists("Account/" + self.username):
                    os.mkdir("Account/" + self.username)
            elif username_fromFile != username:
                self.update_btn_status(False)  # 禁用按钮
                thread1 = Thread(target=inform_thread)
                thread2 = Thread(target=login_check_thread)
                thread1.start()
                thread2.start()
            else:
                self.update_status(False)
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
        self.update_btn_status(True)  # 启用按钮
        self.msgBox.button(QMessageBox.Ok).animateClick()
        self.update_status(True)
        self.mySignals.login2main_signal.emit()
        if not os.path.exists("Account/" + self.username):
            os.mkdir("Account/" + self.username)

    def fail_login(self):
        """
        登录失败

        :return: None
        """
        self.update_btn_status(True)  # 启用按钮
        self.msgBox.button(QMessageBox.Ok).animateClick()
        self.update_status(False)
        QMessageBox.critical(self.ui, '错误', '登录失败')

    def time_out(self):
        """
        登录超时

        :return: None
        """
        self.update_btn_status(True)
        self.msgBox.button(QMessageBox.Ok).animateClick()
        self.update_status(False)
        QMessageBox.critical(self.ui, '错误', '连接超时')

    def update_btn_status(self, status):
        """
        update all buttons' status here

        :param status: button status
        :return: None
        """
        self.ui.Login_btn.setEnabled(status)
        self.ui.auto_login_btn.setEnabled(status)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_login_ui()
    window.ui.show()
    app.exec_()
