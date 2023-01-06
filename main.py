#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication

from Signal import MySignals
from main_login import Main_login_ui
from main_ui import Main_ui


class Main:
    def __init__(self):
        """
        实例化对象
        """
        self.__setup_ui()

    def __setup_ui(self):
        """
        设置界面
        """
        # 类属性
        self.login_ui = Main_login_ui()
        self.main_ui = Main_ui()
        self.mySignals = MySignals()

        # 信号与槽连接
        self.login_ui.ui.Login_btn.clicked.connect(self.login)
        self.login_ui.ui.passwd.returnPressed.connect(self.login)
        self.mySignals.login2main_signal.connect(self.login2main)

    def login(self):
        """
        登录

        :return: None
        """

        def thread():
            """
            检测登录状态线程
            """
            while True:
                if self.login_ui.login_status:
                    self.mySignals.login2main_signal.emit()
                    break

        t = Thread(target=thread)
        t.start()

    def login2main(self):
        """
        登录成功后，将登录界面关闭，显示主界面

        :return: None
        """
        self.login_ui.ui.close()
        self.main_ui.ui.show()
        self.main_ui.setup_ui(self.login_ui.username, self.login_ui.last_sync_time)


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
