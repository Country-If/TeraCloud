#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


class Main_ui:
    """main UI"""

    def __init__(self):
        """
        实例化对象
        """
        # 动态加载界面
        self.ui = uic.loadUi("UI/main_ui.ui")

        # 类属性

    def setup_ui(self, username, last_sync_time):
        self.ui.main_account.setText(username)
        self.ui.last_sync.setText(last_sync_time)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_ui()
    window.ui.show()
    app.exec_()
