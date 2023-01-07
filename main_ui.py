#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem


class Main_ui:
    """main UI"""

    def __init__(self):
        """
        实例化对象
        """
        # 动态加载界面
        self.ui = uic.loadUi("UI/main_ui.ui")

        # 类属性
        self.login_status = True

        # 信号与槽连接
        self.ui.logout_btn.clicked.connect(self.logout)

    def update_status(self, status):
        """
        更新登录状态

        :param status: 登录状态
        :return: None
        """
        self.login_status = status

    def setup_ui(self, username, capacity, last_sync_time):
        """
        设置界面

        :param username: 用户名
        :param capacity: 容量
        :param last_sync_time: 最后同步时间
        :return: None
        """
        self.ui.main_account.setText(username)
        self.ui.last_sync.setText(last_sync_time)
        self.add_row_information(username, capacity)  # TODO: 设置表头伸缩和行列号隐藏等，UI界面美化

    def logout(self):
        """
        注销登录

        :return: None
        """
        self.update_status(False)

    def add_row_information(self, userId, capacity):
        """
        添加行信息

        :param userId: 用户名
        :param capacity: 容量
        :return: None
        """
        self.ui.tableWidget.insertRow(0)
        self.ui.tableWidget.setItem(0, 0, QTableWidgetItem(userId))
        self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(capacity))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_ui()
    window.ui.show()
    app.exec_()
