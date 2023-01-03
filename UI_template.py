#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


class ui:
    """***"""

    def __init__(self):
        """
        实例化对象
        """
        # 动态加载界面
        self.ui = uic.loadUi("UI/***.ui")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ui()
    window.ui.show()
    app.exec_()
