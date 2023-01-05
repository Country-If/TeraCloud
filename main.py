#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

from PyQt5.QtWidgets import QApplication
import sys

from main_login import Main_login_ui
from main_ui import Main_ui


class Main:
    def __init__(self):
        self.__setup_ui()

    def __setup_ui(self):
        self.login_ui = Main_login_ui()
        self.main_ui = Main_ui()

        self.login_ui.ui.Login_btn.clicked.connect(self.login)
        self.login_ui.ui.passwd.returnPressed.connect(self.login)

    def login(self):
        if self.login_ui.login_status:
            self.main_ui.ui.show()


def main():
    app = QApplication(sys.argv)
    window = Main()
    window.login_ui.ui.show()
    app.exec_()


if __name__ == '__main__':
    main()
