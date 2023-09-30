#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import os
import sys

from PyQt5.QtWidgets import QApplication

from main_login import Main_login_ui
from main_ui import Main_ui


class Main:
    def __init__(self):
        """
        实例化对象
        """
        # 类属性
        self.main_login_ui = Main_login_ui()
        self.main_ui = Main_ui()
        self.main_ui.browser = "Chrome"

        # 信号与槽连接
        self.main_login_ui.mySignals.login2main_signal.connect(self.login2main)
        self.main_login_ui.ui.auto_login_btn.clicked.connect(self.auto_login)
        self.main_ui.ui.logout_btn.clicked.connect(self.logout)
        self.main_ui.ui.del_main_btn.clicked.connect(self.logout)
        self.main_login_ui.ui.Chrome_btn.toggled.connect(self.set_browser)
        self.main_login_ui.ui.Firefox_btn.toggled.connect(self.set_browser)
        self.main_login_ui.ui.Edge_btn.toggled.connect(self.set_browser)

    def auto_login(self):
        """
        auto login

        :return: None
        """
        if self.main_login_ui.login_status:
            self.login2main()
            self.main_ui.sync_time()

    def update_tableWidgets(self):
        """
        update tableWidgets when auto login

        :return: None
        """
        if os.path.exists("../Account/" + self.main_login_ui.username):
            file_list = os.listdir("../Account/" + self.main_login_ui.username)
            for file in file_list:
                with open("../Account/" + self.main_login_ui.username + '/' + file, 'r') as f:
                    username = f.readline().strip()
                    f.readline()
                    capacity = f.readline().strip()
                    self.main_ui.add_row_information(username, capacity)
                    self.main_ui.add_del_sum_capacity(capacity, '+')

    def login2main(self):
        """
        登录成功后，将登录界面关闭，显示主界面

        :return: None
        """
        self.main_login_ui.ui.close()
        self.main_ui.ui.show()
        self.main_ui.setup_ui(self.main_login_ui.username, self.main_login_ui.capacity)
        self.update_tableWidgets()

    def logout(self):
        """
        注销登录

        :return: None
        """

        self.main_ui.logout()
        self.main_login_ui.update_status(False)
        self.main2login()

    def main2login(self):
        """
        注销登录后，将主界面关闭，显示登录界面

        :return: None
        """
        self.main_ui.ui.close()
        self.main_login_ui.ui.show()
        if not self.main_login_ui.remember_password:
            self.main_login_ui.ui.passwd.clear()

    def set_browser(self):
        """
        set browser

        :return: None
        """
        if self.main_login_ui.ui.Chrome_btn.isChecked():
            self.main_ui.browser = "Chrome"
        elif self.main_login_ui.ui.Firefox_btn.isChecked():
            self.main_ui.browser = "Firefox"
        elif self.main_login_ui.ui.Edge_btn.isChecked():
            self.main_ui.browser = "Edge"


def main():
    """
    主程序入口

    :return: None
    """
    app = QApplication(sys.argv)
    window = Main()
    window.main_login_ui.ui.show()
    app.exec_()


if __name__ == '__main__':
    main()
