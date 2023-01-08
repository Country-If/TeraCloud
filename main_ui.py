#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView


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
        # 设置表格头的伸缩模式，让表格铺满整个QTableWidget控件
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏表格的行列号
        self.ui.tableWidget.verticalHeader().setHidden(True)
        self.add_row_information(username, capacity)

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
