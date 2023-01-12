#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import sys
import os

from PyQt5.QtWidgets import QApplication

from Signal import MySignals
from main_login import Main_login_ui
from main_ui import Main_ui


class Main:
    def __init__(self):
        """
        实例化对象
        """
        # 类属性
        self.login_ui = Main_login_ui()
        self.main_ui = Main_ui()
        self.mySignals = MySignals()

        # 信号与槽连接
        self.login_ui.mySignals.login2main_signal.connect(self.login2main)
        self.login_ui.ui.auto_login_btn.clicked.connect(self.auto_login)
        self.mySignals.login2main_signal.connect(self.login2main)
        self.main_ui.ui.logout_btn.clicked.connect(self.logout)

    def auto_login(self):
        """
        auto login

        :return: None
        """
        if self.login_ui.login_status:
            self.login2main()
            self.main_ui.sync_time()

    def update_tableWidgets(self):
        """
        update tableWidgets when auto login

        :return: None
        """
        if os.path.exists("Account/" + self.login_ui.username):
            file_list = os.listdir("Account/" + self.login_ui.username)
            for file in file_list:
                with open("Account/" + self.login_ui.username + '/' + file, 'r') as f:
                    username = f.readline().strip()
                    f.readline().strip()
                    capacity = f.readline().strip()
                    self.main_ui.add_row_information(username, capacity)
                    self.main_ui.update_sum_capacity(capacity)

    def login2main(self):
        """
        登录成功后，将登录界面关闭，显示主界面

        :return: None
        """
        self.login_ui.ui.close()
        self.main_ui.ui.show()
        self.main_ui.setup_ui(self.login_ui.username, self.login_ui.capacity)
        self.update_tableWidgets()

    def logout(self):
        """
        注销登录

        :return: None
        """

        self.main_ui.logout()
        self.login_ui.update_status(False)
        self.main2login()

    def main2login(self):
        """
        注销登录后，将主界面关闭，显示登录界面

        :return: None
        """
        self.main_ui.ui.close()
        self.login_ui.ui.show()
        if not self.login_ui.remember_password:
            self.login_ui.ui.passwd.clear()


def main():
    """
    主程序入口

    :return: None
    """
    app = QApplication(sys.argv)
    window = Main()
    window.login_ui.ui.show()
    app.exec_()


if __name__ == '__main__':
    main()
