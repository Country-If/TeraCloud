#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import sys
from threading import Thread

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView, QMessageBox

from Signal import MySignals
from common import *
from subAccount_login import SubAccount_login_ui


class Main_ui:
    """main UI"""

    # TODO: add account
    # TODO: del account
    # TODO: del main account
    # TODO: sync capacity

    def __init__(self):
        """
        实例化对象
        """
        # 动态加载界面
        self.ui = uic.loadUi("UI/main_ui.ui")
        self.sub_ui = None

        # 类属性
        self.login_status = True
        self.username = None
        self.mySignals = MySignals()

        # 信号与槽连接
        self.ui.logout_btn.clicked.connect(self.logout)
        self.ui.add_btn.clicked.connect(self.add_account)
        self.mySignals.login_success_signal.connect(self.sub_login)

    def sub_login(self):
        """
        update UI when subAccount successfully login

        :return: None
        """
        self.add_row_information(self.sub_ui.add_username, self.sub_ui.capacity)
        # self.sync_time()
        # TODO: update sum capacity

    def add_account(self):
        """
        add an account

        :return: None
        """
        if not os.path.exists("Account/" + self.username):
            os.mkdir("Account/" + self.username)
        self.sub_ui = SubAccount_login_ui(self.username)
        self.sub_ui.exec_()

        def sub_login_thread():
            while not self.sub_ui.login_status:
                if self.sub_ui.login_status:
                    self.mySignals.login_success_signal.emit()
                    break

        thread = Thread(target=sub_login_thread)
        thread.start()

    def update_status(self, status):
        """
        更新登录状态

        :param status: 登录状态
        :return: None
        """
        self.login_status = status

    def setup_ui(self, username, capacity):
        """
        设置界面

        :param username: 用户名
        :param capacity: 容量
        :return: None
        """

        self.username = username
        self.ui.main_account.setText(username)
        self.sync_time()
        # 设置表格头的伸缩模式，让表格铺满整个QTableWidget控件
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏表格的行列号
        self.ui.tableWidget.verticalHeader().setHidden(True)
        self.add_row_information(username, capacity)
        self.ui.sum_label.setText(capacity)

    def logout(self):
        """
        注销登录

        :return: None
        """
        self.update_status(False)
        self.clearTable()

    def clearTable(self):
        """
        清空表格

        :return: None
        """
        self.ui.tableWidget.clearContents()
        self.ui.tableWidget.setRowCount(0)

    def add_row_information(self, userId, capacity):
        """
        insert a row information from the end

        :param userId: 用户名
        :param capacity: 容量
        :return: None
        """
        insertRow = self.ui.tableWidget.rowCount()
        self.ui.tableWidget.insertRow(insertRow)

        userId_Item = QTableWidgetItem(userId)
        userId_Item.setFlags(Qt.ItemIsEnabled)  # 设置单元格为只读
        userId_Item.setTextAlignment(Qt.AlignCenter)  # 设置文本内容居中
        self.ui.tableWidget.setItem(insertRow, 0, userId_Item)

        capacity_Item = QTableWidgetItem(capacity)
        capacity_Item.setFlags(Qt.ItemIsEnabled)  # 设置单元格为只读
        capacity_Item.setTextAlignment(Qt.AlignCenter)  # 设置文本内容居中
        self.ui.tableWidget.setItem(insertRow, 1, capacity_Item)

    def sync_time(self):
        """
        set sync time in UI

        :return: None
        """
        sync_t = load_sync_time()
        if sync_t is None:
            QMessageBox.critical(self.ui, '错误', '无法加载last_sync_time文件')
        else:
            self.ui.last_sync.setText(sync_t)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_ui()
    window.ui.show()
    app.exec_()
